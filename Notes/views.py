from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.
class Pages(View):
	def get(self, request):
		html = "<html><body><h2>Welcome to our Task Management System</h2></body></html>"
		return HttpResponse(html, status=200)
	