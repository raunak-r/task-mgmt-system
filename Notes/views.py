# Core Django Imports
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.template.loader import render_to_string
from django.views.generic import View

# Imports from models.py of this app
from models import Task
from models import Comment

# Create your views here.
class Pages(View):
	def get(self, request):
		html = render_to_string('base.html')
		return HttpResponse(html, status=200)

class Tasks(View):
	def createTaskStr(self, t):		#Format the string for printing purposes
		cmntList = Comment.objects.filter(taskId_id = t.taskId)
		str = ('LABEL = %s</br>\
				<b>TASK ID = %d</b></br>\
				DUE DATE = <b>%s</b></br>\
				TITLE = <b>%s</b></br>\
				DESCRIPTION = %s</br>\
				AUTHOR = %s</br>\
				COMMENT = %s</br>'
				% (t.label, t.taskId, t.dueDate, t.title, t.description, t.createdBy, t.comments))

		# ADD COMMENT ATTRIBUTES
		if not cmntList:	#WHEN THERE ARE NO ADDITIONAL COMMENTS
			str = str + '</br></br>'
		else:
			str = str + 'Addn. Comments</br>'
			for c in cmntList:
				str = str + ('Id = %d\
				<b>Text =</b> %s\
				<b>Posted By =</b> %s</br>'
				%(c.commentId, c.commentText, c.createdBy))

			str = str + '</br></br>'
		return str

	def get(self, request):		
		# - Get the task details (GET /tasks/<task_id>/)
		# http://127.0.0.1:8000/Notes/tasks/?id=6
		id = int(request.GET.get('id', '0'))
		if id != 0:
			task = []
			tasks = Task.objects.filter(taskId=id)
			for t in tasks:
				# Send the Task Object to receive a nicely formatted string for printing
				string = self.createTaskStr(t)
				task.append(string)
			return HttpResponse(task, status=200)

		# - Get all tasks grouped by list (GET / tasks/)
		# http://127.0.0.1:8000/Notes/tasks/
		taskList = []
		Labels = ['<h3>***TODO***</h3>', '<h3>***DOING***</h3>', '<h3>***DONE***</h3>']

		for i in range(1,4):
			taskList.append(Labels[i-1])
			tasks = Task.objects.filter(label=i)
			for t in tasks:
				# Send the Task Object to receive a nicely formatted string for printing
				str = self.createTaskStr(t)	
				taskList.append(str)
				
		return HttpResponse(taskList, status=200)

	def post(self, request):		# - Create a task (POST /tasks/
		task = request.POST
		
		# RECEIVE THE VALUES
		t = task['title']
		d = task['desc']
		l = task['label']
		col = task['color']
		co = task['comments']
		cby = task['author']
		due = task['due']

		# CANNOT BE BLANK = Title. Label. CreatedBy. DueDate
		if t == '' or l == '' or cby == '' or due == '':
			return HttpResponse('Title, Label, CreatedBy, Due Date are mandatory Fields.', status=200)

		entry = Task(title = t, description = d, label = l, color = col, comments = co, createdBy = cby, dueDate = due)
		entry.save()
		return HttpResponse('Success', status=200)

	def put(self, request):		# - Edit a task (PUT /tasks/<task_id>/)
		# http://127.0.0.1:8000/Notes/tasks/?id=3

		id = int(request.GET.get('id'))
		entry = Task.objects.filter(taskId=id)

		taskDetails = QueryDict(request.body)
		if 'title' in taskDetails.keys():
			t = taskDetails['title']
			entry.update(title = t)
		if 'desc' in taskDetails.keys():
			d = taskDetails['desc']
			entry.update(description = d)
		if 'label' in taskDetails.keys():
			l = taskDetails['label']
			entry.update(label = l)
		if 'color' in taskDetails.keys():
			col = taskDetails['color']
			entry.update(color = col)
		if 'comments' in taskDetails.keys():
			co = taskDetails['comments']
			entry.update(comments = co)
		if 'due' in taskDetails.keys():
			due = taskDetails['due']
			entry.update(dueDate = due)

		return HttpResponse('Task Updated Successfully', status=200)

	def delete(self, request):		# Delete a task (DELETE /tasks/<task_id>/)
		id = int(request.GET.get('id'))
		task = Task.objects.get(taskId=id)
		task.delete()
		return HttpResponse('Task Deleted', status=200)


class Comments(View):
	def get(self, request):		#Get all Comments
		# http://127.0.0.1:8000/Notes/comments/
		comments = Comment.objects.all()
		cmntList = []

		# SHOWS COMMENTS ORDERED BY taskId_id
		for t in comments:
			tasks = Task.objects.get(taskId = t.taskId_id)
			str = ('COMMENT ID = %d</br>\
					TASK_ID = %s</br>\
					TASK_TITLE = <b>%s</b></br>\
					COMMENT = %s</br>\
					AUTHOR = %s</br>\
					LAST UPDATED ON = %s</br>\
					</br></br>'
					% (t.commentId, t.taskId_id, tasks, t.commentText, t.createdBy, t.UpdatedOn))
			cmntList.append(str)
		return HttpResponse(cmntList, status=200)

	# def get(self, request, id):		#Get Comment by id in url
	# 	# http://127.0.0.1:8000/Notes/comments/
	# 	comments = Comment.objects.filter(taskId = id)
	# 	cmntList = []
	# 	for c in comments:
	# 		cmntList.append(c)
	# 		cmntList.aplapend("</br>")
	# 	return HttpResponse(cmntList, status=200)

	def post(self, request):	# Post a new Comment
		c = request.POST
		tid = c['tid']
		cby = c['author']
		ctext = c['text']
		
		if ctext == '' or tid == '' or cby == '':
			return HttpResponse('Comment, TaskId, Author are mandatory Fields.')

		entry = Comment(taskId_id = tid, createdBy = cby, commentText = ctext)
		entry.save()
		return HttpResponse('Success', status=200)

	def put(self, request):		# Edit a comment
		# http://127.0.0.1:8000/Notes/comments/?id=1
		id = int(request.GET.get('id'))
		entry = Comment.objects.filter(commentId=id)
		# print(entry)

		c = QueryDict(request.body)
		c = str(c['comment'])
		if c == '':
			return HttpResponse('Please give the new comment', status=200)
		entry.update(commentText = c)
		return HttpResponse('Comment Updated Successfully', status=200)