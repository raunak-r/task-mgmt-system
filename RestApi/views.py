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
	filename = request.GET.get('file', 'bill1.jpg')
	filename = 'Bills/' + filename

	# export GOOGLE_APPLICATION_CREDENTIALS="/Users/raunakritesh/Documents/HappayProjects/task-mgmt-sys/visionapi.json"
	# 1. TO use handwriting algo
		# https://cloud.google.com/vision/docs/detecting-text#vision-text-detection-python
	

	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file-receipt to annotate
	filename = os.path.join(os.path.dirname(__file__), filename)

	# Loads the image-receipt into memory
	with io.open(filename, 'rb') as image_file:
	    content = image_file.read()
	image = types.Image(content=content)

	# # 1. Label Detection
	# response = client.detection(image=image)
	# print(response)
	# labels = response.label_annotations
	# # print(labels)
	# for l in labels:
	# 	print(l.description)

	# # 2. Text Detection
	response = client.text_detection(image=image)
	# print(response)

	texts = response.text_annotations
	# print(texts)	# print all the dictionaries in the text_annotations
	print(texts[0].description)

	return HttpResponse('Done, Check terminal.')