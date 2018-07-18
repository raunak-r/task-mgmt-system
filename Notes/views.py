# Core Django Imports
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.views.generic import View
from django.db.models import Count

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
				COMMENT = <i>%s</i></br>'
				% (t.label, t.taskId, t.dueDate, t.title, t.description, t.createdBy, t.comments))

		# ADD COMMENT ATTRIBUTES
		if not cmntList:	#WHEN THERE ARE NO ADDITIONAL COMMENTS. WHEN SET IS EMPTY
			str = str + '</br></br>'
		else:		#WHEN THE QUERY SET IS NOT EMPTY
			str = str + 'Addn. Comments</br>'
			for c in cmntList:
				str = str + ('Id = %d\
				<b>Text =</b> <i>%s</i>\
				<b>Posted By =</b> %s</br>'
				%(c.commentId, c.commentText, c.createdBy))

			str = str + '</br></br>'
		return str

	def get(self, request):
		# - Get the task details (GET /tasks/<task_id>/)
		# http://127.0.0.1:8000/Notes/tasks/?id=6
		try:	
			id = int(request.GET.get('id', '0'))
			if id != 0:
				task = []
				tasks = Task.objects.get(taskId=id, isDeleted = False)
				# Send the Task Object to receive a nicely formatted string for printing
				string = self.createTaskStr(tasks)
				task.append(string)

				return HttpResponse(task, status=200)

			# - Get all tasks grouped by list (GET / tasks/)
			# http://127.0.0.1:8000/Notes/tasks/
			taskList = []
			Labels = ['<h3>***TODO***</h3>', '<h3>***DOING***</h3>', '<h3>***DONE***</h3>']

			for i in range(1,4):
				taskList.append(Labels[i-1])
				tasks = Task.objects.filter(label=i, isDeleted = False)
				if not tasks: #i.e. Query Set returned 0 Objects
					taskList.append("<b>No Tasks Present in Database</br></b>") 
				for t in tasks:
					# Send the Task Object to receive a nicely formatted string for printing
					str = self.createTaskStr(t)	
					taskList.append(str)
			return HttpResponse(taskList, status=200)

		except Task.DoesNotExist as e:
			return HttpResponse("Task Not Found", status=200)
		except Exception as e:
			return HttpResponse(e, status=400)

	def post(self, request):		# - Create a task (POST /tasks/
		try:
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
				return HttpResponse('title, label, author, due Date are mandatory Fields.', status=200)

			entry = Task(title = t, description = d, label = l, color = col, comments = co, createdBy = cby, dueDate = due)
			entry.save()
			return HttpResponse('Success', status=200)
		except Exception, e:
			error = "Please provide all the details:- 'title', 'desc',\
					'label', 'color', 'comments', 'author', 'due' where\
					Title, Label, CreatedBy, Due Date are mandatory Fields."
		return HttpResponse(error, status=500)

	def put(self, request):		# - Edit a task (PUT /tasks/<task_id>/)
		# http://127.0.0.1:8000/Notes/tasks/?id=3
		try:
			id = int(request.GET.get('id'))
			entry = Task.objects.get(taskId=id)

			taskDetails = QueryDict(request.body)
			if not taskDetails:
				return HttpResponse('Please provide something to change. Attributes can be given in the same format as in POST', status=200)

			if 'title' in taskDetails.keys():
				entry.title = taskDetails['title']
			if 'desc' in taskDetails.keys():
				entry.description = taskDetails['desc']
			if 'label' in taskDetails.keys():
				entry.label = taskDetails['label']
			if 'color' in taskDetails.keys():
				entry.color = taskDetails['color']
			if 'comments' in taskDetails.keys():
				entry.comments = taskDetails['comments']
			if 'due' in taskDetails.keys():
				entry.dueDate = taskDetails['due']

			entry.save()
			return HttpResponse('Task Updated Successfully', status=200)
		except Task.DoesNotExist as e:
			return HttpResponse("Task Not Found. Therefore cannot be updated", status=200)
		except Exception as e:
			return HttpResponse(e, status=200)

	def delete(self, request):		# Delete a task (DELETE /tasks/<task_id>/)
		try:	
			id = int(request.GET.get('id', '0'))
			if id == 0:
				return HttpResponse('Please give taskId in the url.', status=200)
			
			task = Task.objects.get(taskId=id)
			task.delete()
			return HttpResponse('Task Deleted', status=200)

		except Task.DoesNotExist as e:
			return HttpResponse('Task Not Found, Cannot be Deleted.', status=200)
		except Exception as e:
			return HttpResponse(e, status=200)	

class Comments(View):
	def get(self, request):		#Get all Comments
		# http://127.0.0.1:8000/Notes/comments/
		try:
			# 1st CHECK IF COMMENTS DB IS EMPTY NOT
			cmntlist = Comment.objects.all()
			if not cmntlist:
					return HttpResponse('No Comments in the Database.', status=200)

			# IF NOT EMPTY
			comments = []
			for i in range(1,4):
				tasks = Task.objects.filter(label=i)	#Read all tasks by label
				for t in tasks:
					cmntList = Comment.objects.filter(taskId_id = t.taskId) #filter comments by that Task ID
					str = ''
					if cmntList:	#If cmntlist NOT empty
						str = ('Task Id = %d\
								<b>Title = %s</b></br>'
								% (t.taskId, t.title))
						for c in cmntList:
							str = str + ('Id = %d\
							Text = <i>%s</i></br>\
							Posted By = %s\
							Date Posted = %s</br>'
							%(c.commentId, c.commentText, c.createdBy, c.createdOn))
						str = str + '</br>'
					comments.append(str)
			return HttpResponse(comments, status=200)
		except Exception as e:
			return HttpResponse(e, status=400)

	# def get(self, request, id):		#Get Comment by id in url
	# 	# http://127.0.0.1:8000/Notes/comments/
	# 	comments = Comment.objects.filter(taskId = id)
	# 	cmntList = []
	# 	for c in comments:
	# 		cmntList.append(c)
	# 		cmntList.aplapend("</br>")
	# 	return HttpResponse(cmntList, status=200)

	def post(self, request):	# Post a new Comment
		try:	
			c = request.POST
			tid = c['tid']
			cby = c['author']
			ctext = c['text']
			
			if ctext == '' or tid == '' or cby == '':
				return HttpResponse('Comment, TaskId, Author are mandatory Fields.')

			entry = Comment(taskId_id = tid, createdBy = cby, commentText = ctext)
			entry.save()
			return HttpResponse('Success', status=200)
		except Exception as e:
			return HttpResponse('Please Provide a Task Id which exists in the Database. text, tid, author are mandatory Fields.', status=200)

	def put(self, request):		# Edit a comment
		# http://127.0.0.1:8000/Notes/comments/?id=1
		try:
			id = int(request.GET.get('id'))
			entry = Comment.objects.get(commentId=id)

			c = QueryDict(request.body)
			c = str(c['comment'])
			if c == '':
				return HttpResponse('Please give the new comment', status=200)
			entry.commentText = c
			entry.save()
			return HttpResponse('Comment Updated Successfully', status=200)

		except Comment.DoesNotExist, e:
			return HttpResponse("Comment Not Found. Therefore cannot be updated", status=200)
		except Exception as e:
			return HttpResponse('Provide commentId in the url, and new comment in comment attribute.', status=200)

class Statistics(View):
	def get(self, request):
		c = Comment.objects.values('taskId').annotate(total=Count('taskId')).order_by('-total')
		# print(c)
		# print(c[0])
		# print(c[0].get('taskId'))

		e = Task.objects.get(taskId = c[0].get('taskId'))
		return HttpResponse('Task with maximum comments is = <b>%s</b> with %d Comments' %(e.title, c[0].get('total')), status=200)

