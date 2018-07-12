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
	def get(self, request):		

	# - Get the task details (GET /tasks/<task_id>/)
		id = int(request.GET.get('id', '0'))
		if id != 0:
			task = []
			tasks = Task.objects.filter(taskId=id)
			for t in tasks:
				str = ('DUE DATE = %s</br>\
				TITLE = %s</br>\
				DESCRIPTION = %s</br>\
				AUTHOR = %s</br>\
				</br></br>'
				% (t.dueDate, t.title, t.description, t.createdBy))
				task.append(str)
			return HttpResponse(task, status=200)

	# - Get all tasks grouped by list (GET / tasks/)
		taskList = []
		Labels = ['***TODO***</br></br>', '***DOING***</br></br>', '***DONE***</br></br>']

		for i in range(1,4):
			taskList.append(Labels[i-1])
			tasks = Task.objects.filter(label=i)
			# print(tasks)
			for t in tasks:
				str = ('TASK %d</br>\
					DUE DATE = %s</br>\
				TITLE = %s</br>\
				DESCRIPTION = %s</br>\
				AUTHOR = %s</br>\
				</br></br>'
				% (t.taskId, t.dueDate, t.title, t.description, t.createdBy))

				taskList.append(str)
				
		return HttpResponse(taskList, status=200)


	def post(self, request):		# - Create a task (POST /tasks/
		task = request.POST
		
		# RECEIVE THE VALUES
		t = task['title']
		d = task['desc']
		l = task['label']
		col = task['color']
		com = task['comments']
		cby = task['author']
		due = task['due']

		# CANNOT BE BLANK = Title. Label. CreatedBy. DueDate
		if t == '' or l == '' or cby == '' or due == '':
			return HttpResponse('Title, Label, CreatedBy, Due Date are mandatory Fields.')

		entry = Task(title = t, description = d, label = l, color = col, comments = com, createdBy = cby, dueDate = due)
		entry.save()
		return HttpResponse('Success', status=200)

# 	def put(self, request):
# 		# - Edit a task (PUT /tasks/<task_id>/)

	def delete(self, request):		# Delete a task (DELETE /tasks/<task_id>/)
		id = int(request.GET.get('id'))
		task = Task.objects.get(taskId=id)
		task.delete()
		return HttpResponse('Task Deleted', status=200)


# class Comments(View):
# 	def put(self, request):
# 		# Add / edit a comment