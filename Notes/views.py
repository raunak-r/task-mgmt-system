# Core Django Imports
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Imports from models.py of this app
from models import Task
from models import Comment

# Create your views here.
class Pages(View):
	def get(self, request):
		html = "<html><body><h2>Welcome to our Task Management System</h2></body></html>"
		return HttpResponse(html, status=200)

class Tasks(View):
	def get(self, request):		# - Get all tasks grouped by list (GET / tasks/)
		taskList = []
		Labels = ['***TODO***</br></br>', '***DOING***</br></br>', '***DONE***</br></br>']

		for i in range(1,4):
			taskList.append(Labels[i-1])
			tasks = Task.objects.filter(label=i)
			# print(tasks)
			for t in tasks:
				str = ('DUE DATE = %s</br>\
				TITLE = %s</br>\
				DESCRIPTION = %s</br>\
				AUTHOR = %s</br>\
				</br></br>'
				% (t.dueDate, t.title, t.description, t.createdBy))

				taskList.append(str)
				
		return HttpResponse(taskList, status=200)


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