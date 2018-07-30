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
	texts = response.text_annotations #Get the text_annotations Dicts
	# print(texts)	# print all the dictionaries in the text_annotations
	print(texts[0].description)

	amounts = []
	regex = {
	'cost' : "[0-9]+[.][0-9]+",
	# 'gst' : "",
	# 'date' : "",
	'currSym' : "$| ",
	'extra' : "^0-9.",
	}

	t1 = time.time()
	for t in texts:
		# print(t)
		text = (t.description).encode('ascii', 'ignore')
		# if re.match(r'[N|n]et|[A|a]mount|[T|t]otal', text):
		# 	print(text)
		if re.match('[0-9]+[.][0-9]+', text):
			print(text)			
			# Clean it to retain only numbers
			text = re.sub('[^0-9.]', '', text)

			amounts.append(float(text))

	print('TOTAL = %0.2f' % max(amounts))
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