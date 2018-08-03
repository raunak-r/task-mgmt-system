from django.shortcuts import render
import requests
import json
from django.http import JsonResponse, HttpResponse

# Imports for VisionApi
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import re, math
import time
import operator


def ip(request):
	# p/w = raunak. username = raunakritesh.india@gmail.com

	# Read Api.json. Done this way to not to expose the api keys to public.
	with open('./../api.json') as json_data:
		apiData = json.load(json_data)

	ipstackApi = apiData['ipstack']	#Store the api's
	gmapsApi = apiData['gmaps']


	response = requests.get('http://api.ipstack.com/check?access_key=%s' % ipstackApi)
	geodata = response.json()
	# pdb.set_trace()
	
	return render(request, 'restapi/ip.html', {
		'ip': geodata['ip'], 'country': geodata['country_name'],
		'latitude': geodata['latitude'], 'longitude': geodata['longitude'],
		'api_key': ('%s' % gmapsApi)
    })

# export GOOGLE_APPLICATION_CREDENTIALS="/Users/raunakritesh/Documents/HappayProjects/task-mgmt-sys/vision_key_happay.json"
def visionApiFile(request):
	t0 = time.time()

	# 1. Give file name manually
	filename = request.GET.get('file', 'bill1.jpg')
	extractText(filename, 0)

	print('SCRIPT RUN TIME = %s' %(time.time() - t0))
	return HttpResponse('Done')

def visionApiScript(request):
	t0 = time.time()

	### 2. Read receipts.txt and do the thing
	with io.open('RestApi/Receipts/receipts.txt', 'r') as receipt:
		for line in receipt:
			array = re.split(r'\s+', line)
			filename = array[0]
			totalCost = array[1]
			extractText(filename, totalCost)

	print('SCRIPT RUN TIME = %s' %(time.time() - t0))
	return HttpResponse('Done')



def extractText(filename, totalOriginal):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file-receipt to annotate
	currentDir = os.path.dirname(__file__)
	filename = 'Receipts/Bills/' + filename
	filename = os.path.join(currentDir, filename)
	print(filename)

	# Loads the image-receipt into memory
	with io.open(filename, 'rb') as image_file:
	    content = image_file.read()
	image = types.Image(content=content)
	

	# # 1. LABEL DETECTION
	# response = client.label_detection(image=image)
	# # print(response)
	# # print(response)
	# labels = response.label_annotations	#Get the label_annotations Dicts
	# # print(labels)
	# for l in labels:
	# 	print('%s = %0.2f' % (l.description, l.score*100))

	# 2. TEXT DETECTION
	# TO use handwriting algo
		# https://cloud.google.com/vision/docs/detecting-text#vision-text-detection-python
	response = client.text_detection(image=image)
	extractTotal(response, totalOriginal)

	# Output the received response to a txt file
	with open(currentDir + '/Receipts/response.txt', 'w') as outfile:
		outfile.write(str(response))
	outfile.close()
	image_file.close()
	return


def extractTotal(response, totalOriginal):	
	textDicts = response.text_annotations #Get the text_annotations Dicts

	regex = {
		'text' : "net|total|amount",
		# 'ignoreText' : "change|"
		'cost' : "[$]{0,1}([0-9]+[,])*[0-9]+[.][0-9]+",
		'percent' : "[0-9]+[.][0-9]+[%]",
		# 'gst' : "GST[.][A-Z0-9]{15}",
		'date' : "",
		'currSym' : "${0,1}",
		'extra' : "^0-9.",
	}

	t1 = time.time()	#TIME THIS LOOP

	texts = []	#Store all dicts matching regex['text']
	amounts = []	#TO store all dicts matching regex['cost']
	amountsDist = []	#Store by Decreasing distance
	amountsArea = []	#Store by Decreasing Area

	for t in textDicts:
		description = (t.description).encode('ascii', 'ignore')	#Convert to ascii.

		# # Calculate levenshtein distance and convert for regex['text']
		# if len(description) <= 6 && >=3:
		# 	levenshtein(description)

		if re.match(regex['text'], description, re.I):
			d = {
				'description' : description,
				'bounding_poly' : t.bounding_poly,
			}
			texts.append(d)
		
		if re.match(regex['cost'], description):
			if re.match(regex['percent'], description):
				continue
			description = re.sub('[^0-9.]', '', description)	# Clean it to retain only numbers
			d = {
				'description' : float(description),
				'bounding_poly' : t.bounding_poly,
			}
			amounts.append(d)

	# Sort amounts dicts in decreasing order and select top 5
	amounts.sort(key=operator.itemgetter('description'), reverse = True)
	amounts = amounts[0:6]

	# # Code to extract co-ordinates 
	# print(type(((texts[0])['bounding_poly'].vertices[0]).x))

	# # CHECK 1 Find nearest distance between text and amount
	totalAmount = '' #(amounts[0])['description']	#POSSIBLE that no amount is present in bill
	minDist = 2000
	for i in texts:
		# textX = (i['bounding_poly'].vertices[1].x + i['bounding_poly'].vertices[2].x)/2
		# textY = (i['bounding_poly'].vertices[1].y + i['bounding_poly'].vertices[2].y)/2
		
		for j in amounts:
			# # # 6/10 Score - right mid text - left mid amount 90 seconds
			# amtX = (j['bounding_poly'].vertices[0].x + j['bounding_poly'].vertices[3].x)/2
			# amtY = (j['bounding_poly'].vertices[0].y + j['bounding_poly'].vertices[3].y)/2
			# distance = math.sqrt(math.pow(abs(textX - amtX), 2) + math.pow(abs(textY - amtY), 2))

			# # # 4/10 Score - left bottom text - right bottom amount
			# distX = abs((j['bounding_poly'].vertices[1]).x - (i['bounding_poly'].vertices[0]).x)
			# distY = abs((j['bounding_poly'].vertices[1]).y - (i['bounding_poly'].vertices[0]).y)
			# distance = distY + distX

			# # # 8/10 Score - right bottom text - left bottom amount 70 seconds
			distX = abs((j['bounding_poly'].vertices[0]).x - (i['bounding_poly'].vertices[1]).x)
			distY = abs((j['bounding_poly'].vertices[0]).y - (i['bounding_poly'].vertices[1]).y)
			distance = distY + distX

			# print('%s and %s and %d'
			#  %(i['description'], j['description'], distance))
			if distance < minDist:
				minDist = distance
				amountsDist.insert(0, j)
				totalAmount = j['description']

	# # # CHECK 2 Find MAX AREA of Text
	# for i in amounts:
	# 	length = i['bounding_poly'].vertices[1].x - i['bounding_poly'].vertices[0].x
	# 	breadth = i['bounding_poly'].vertices[3].y - i['bounding_poly'].vertices[0].y
	# 	area = length * breadth

	if len(texts) == 0:
		totalAmount = amounts[0]['description']

	# print(textDicts[0].description)
	# print(texts)
	# print(amounts)
	# print(amountsDist)
	print("TOTAL = %s ORIGINAL = %s" %(totalAmount, totalOriginal))
	if totalAmount == totalOriginal:
		print('YAYAAAAA')
	print('TIME to iterate on response.txt = %s' %(time.time() - t1))		







	# ERROR CLASSIFICATION
	# 1. when CHANGE DUE is present
	# 2. Handle comma, currency symbol
	# 3. 

	# # 3. IMAGE PROPERTIES i.e Dominant Colours
	# response = client.image_properties(image=image)

	# 4. LOGO
	# response = client.logo_detection(image=image)

	return