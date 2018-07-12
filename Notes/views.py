from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.
class Pages(View):
	def get(self, request):
		html = "<html><body><h2>Welcome to our Task Management System</h2></body></html>"
		return HttpResponse(html, status=200)

# class Tasks(View):
# 	def get(self, request):
# 		# - Get all tasks grouped by list (GET / tasks/)

# 	def post(self, request):
# 		# - Create a task (POST /tasks/

# 	def put(self, request):
# 		# - Edit a task (PUT /tasks/<task_id>/)

# 	def delete(self, request):
# 		# Delete a task (DELETE /tasks/<task_id>/)

# class TaskSpecific(View):
# 	def get(self, request):
# 		# - Get the task details (GET /tasks/<task_id>/)


# class Comments(View):
# 	def put(self, request):
# 		# Add / edit a comment