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

import re
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

def visionApi(request):
	t0 = time.time()

	filename = request.GET.get('file', 'bill1.jpg')
	filename = 'Bills/' + filename

	# export GOOGLE_APPLICATION_CREDENTIALS="/Users/raunakritesh/Documents/HappayProjects/task-mgmt-sys/visionapi.json"
	# 1. TO use handwriting algo
		# https://cloud.google.com/vision/docs/detecting-text#vision-text-detection-python
	

	# Instantiates a client
	client = vision.ImageAnnotatorClient()
	# The name of the image file-receipt to annotate
	filename = os.path.join(os.path.dirname(__file__), filename)
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
	response = client.text_detection(image=image)
	textDicts = response.text_annotations #Get the text_annotations Dicts
	# print(texts)	# print all the dictionaries in the text_annotations
	# print(textDicts[0].description)

	regex = {
	'cost' : "[0-9]+[.][0-9]+",
	# 'gst' : "",
	# 'date' : "",
	'currSym' : "$| ",
	'extra' : "^0-9.",
	}

	t1 = time.time()	#TIME THIS LOOP


	amountList = []	#store only the amount values
	amounts = []	#TO store all text dicts which match our search
	texts = []	#Store all costs/amounts dicts

	for t in textDicts:
		description = (t.description).encode('ascii', 'ignore')	#Convert to ascii.

		if re.match(r'[n|N][e|E][t|T]|[A|a][m|M][o|O][u|U][n|N][t|T]|[T|t][o|O][t|T][a|A][l|L]', description):
			d = {
				'description' : description,
				'bounding_poly' : t.bounding_poly,
			}
			texts.append(d)
		
		if re.match('[$][0-9]+[.][0-9]+', description):
			description = re.sub('[^0-9.]', '', description)	# Clean it to retain only numbers
			d = {
				'description' : float(description),
				'bounding_poly' : t.bounding_poly,
			}

			amounts.append(d)
			amountList.append(float(description))	#Append only the value

		# If 'CHANGE'/'DISCOUNT'/'COUPON' keyword is present in the bill then do this
		# then don't select any price which has y vertex above first y axis obtained in 

		# 
	# print('TOTAL using max = %0.2f' % max(amountList))

	# # print the amounts before sorting
	# print("Before Sorting")
	# for a in amounts:
	# 	print(a['description'])
	
	# Sort amounts dicts in decreasing order 
	amounts.sort(key=operator.itemgetter('description'), reverse = True)
	
	# # print the amounts AFTER sorting
	# print("After Sorting")
	# for a in amounts:
	# 	print(a['description'])

	amounts = amounts[0:6]
	
	print(texts)
	print(amounts)

	# # Code to extract co-ordinates 
	# print(type(((texts[0])['bounding_poly'].vertices[0]).x))

	# # Find nearest distance between text and amount
	totalAmount = '' #(amounts[0])['description']	#possible that no amount is present in bill
	minDist = 1000
	for i in texts:
		for j in amounts:
			distX = abs((j['bounding_poly'].vertices[1]).x - (i['bounding_poly'].vertices[0]).x)
			distY = abs((j['bounding_poly'].vertices[1]).y - (i['bounding_poly'].vertices[0]).y)
			print('%d' %(distX + distY))
			if (distX + distY) < minDist:
				minDist = distX + distY
				totalAmount = j['description']


	print('USing algo %s' %totalAmount)



	print('Time to iterate on data.txt = %s' %(time.time() - t1))		







	# ERROR CLASSIFICATION
	# 1. when CHANGE DUE is present
	# 2. Handle comma, currency symbol
	# 3. 

	# # 3. IMAGE PROPERTIES i.e Dominant Colours
	# response = client.image_properties(image=image)

	# 4. LOGO
	# response = client.logo_detection(image=image)

	# Output the received response to a txt file
	with open('RestApi/Bills/data.txt', 'w') as outfile:
		outfile.write(str(response))
	outfile.close()
	image_file.close()

	print('Total Time = %s' %(time.time() - t0))		
	return HttpResponse('Done, Check terminal.')