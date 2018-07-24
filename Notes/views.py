# Core Django Imports
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, QueryDict, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.core import serializers

# Imports from Django Db
from django.db import connection
from django.db.models import Count

# Imports from models.py of this app
from models import Task
from models import Comment
from models import User

# Create your views here.
class Pages(View):
	def get(self, request):
		html = render_to_string('base.html')
		return HttpResponse(html, status=200)

class Tasks(View):
	def createTaskDict(self, t):		#Format the dict for Json purposes
		dict = {
			'label' : t.label,
			'title' : t.title,
			'taskId' : t.taskId,
			'dueDate' : t.dueDate,
			'description' : t.description,
			'createdBy' : t.createdBy.username,
			'comments' : t.comments,
		}

		cmntList = Comment.objects.filter(taskId_id = t.taskId)	#get corresponding comments QuerySet
		if cmntList:
			dict.update({'commentList' : []})
			for c in cmntList:
				commentDict = {
					'commentText' : c.commentText,
					'createdBy' : c.createdBy.username,
					'createdOn' : c.createdOn,
				}
				dict['commentList'].append(commentDict)
		return dict

	def get(self, request):
		try:
			id = int(request.GET.get('id', '0'))
			response={}	#Initialize response dict
			response['status'] = '200'
			response['result'] = []

			# - Get the task details (GET /tasks/<task_id>/)
			# http://127.0.0.1:8000/Notes/tasks/?id=6
			if id != 0:
				t = Task.objects.get(taskId=id, isDeleted = False)
				dict = self.createTaskDict(t)
				response['result'].append(dict)
				
				# return render(request, 'tasks.html', response)
				# return render_to_response('tasks.html', {'response': sorted(response.iteritems())})
				return JsonResponse(response, status=200)

			# - Get all tasks grouped by list (GET / tasks/)
			# http://127.0.0.1:8000/Notes/tasks/
			tasks = Task.objects.filter(isDeleted = False).order_by('label')	#Get Not Deleted Tasks
			for t in tasks:				
				dict = self.createTaskDict(t)
				response['result'].append(dict)

			return JsonResponse(response, status=200)

		except Task.DoesNotExist as e:
			return HttpResponse("Task Not Found", status=400)
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

			user = User.objects.get(username = cby) #Get User Instance from given name
			entry = Task(title = t, description = d, label = l, color = col, comments = co, createdBy = user, dueDate = due)
			entry.save()
			return HttpResponse('Success', status=201)
		except User.DoesNotExist, e:
			return HttpResponse('User does not exists in the User Table', status=400)
		except Exception, e:
			error = "Please provide all the details:- 'title', 'desc',\
					'label', 'color', 'comments', 'author', 'due' where\
					Title, Label, CreatedBy, Due Date are mandatory Fields."
		return HttpResponse(error, status=400)

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
			return HttpResponse('Task Updated Successfully', status=201)
		except Task.DoesNotExist as e:
			return HttpResponse("Task Not Found. Therefore cannot be updated", status=400)
		except Exception as e:
			return HttpResponse(e, status=400)

	def delete(self, request):		# Delete a task (DELETE /tasks/<task_id>/)
		try:	
			id = int(request.GET.get('id', '0'))
			if id == 0:
				return HttpResponse('Please give taskId in the url.', status=400)
			
			task = Task.objects.get(taskId=id)
			task.delete()
			return HttpResponse('Task Deleted', status=200)

		except Task.DoesNotExist as e:
			return HttpResponse('Task Not Found, Cannot be Deleted.', status=400)
		except Exception as e:
			return HttpResponse(e, status=400)	

class Comments(View):
	def get(self, request):		#Get all Comments
		# http://127.0.0.1:8000/Notes/comments/
		try:
			response = {}
			response['status'] = 200
			response['result'] = []
			# Get Query Set of all the comments from the Table ordered by Posted First
			cmntList = Comment.objects.all().order_by('-taskId_id')
			# data = serializers.serialize('json', Comment.objects.all().order_by('-taskId_id'), fields=('commentText', 'commentId'))
			# print(data)
			# for an instance in the QuerySet
			for c in cmntList:
				# task = Task.objects.get(taskId = c.taskId_id)	# Get the Task instance by using foreign key
				if c.taskId.isDeleted == True:	#If it is not active then do not add
					continue
				commentDict = {
					'taskId' : c.taskId.taskId,
					'title' : c.taskId.title,
					'commentText' : c.commentText,
					'commentId' : c.commentId,
					'createdBy' : c.createdBy.username,
				}
				response['result'].append(commentDict)
			
			return JsonResponse(response, status=200)
			# return JsonResponse(data, safe=False, status=200)
		 
		except Comment.DoesNotExist, e:
			return HttpResponse('No Comments in the Database.', status=400)
		except Exception as e:
			return HttpResponse(e, status=400)

	def post(self, request):	# Post a new Comment
		try:	
			c = request.POST
			tid = c['tid']
			cby = c['author']
			ctext = c['text']

			if ctext == '' or tid == '' or cby == '':
				return HttpResponse('Comment, TaskId, Author are mandatory Fields.')

			user = User.objects.get(username = cby) #Get User Instance from given name

			# It should be Noted that taskId_id is set by the exact id as defined in the database
			# but createdBy attribute is set by an instance of the User.
			entry = Comment(taskId_id = tid, createdBy = user, commentText = ctext)
			entry.save()
			return HttpResponse('Success', status=201)
		except User.DoesNotExist as e:
			return HttpResponse('User does not exists in the User Table', status=400)
		except Exception as e:
			return HttpResponse('Please Provide a Task Id, and Author which exists in the Database. text, tid, author are mandatory Fields.', status=400)

	def put(self, request):		# Edit a comment
		# http://127.0.0.1:8000/Notes/comments/?id=1
		try:
			id = int(request.GET.get('id'))
			entry = Comment.objects.get(commentId=id)

			c = QueryDict(request.body)
			c = str(c['comment'])
			if c == '':
				return HttpResponse('Please give the new comment', status=400)
			entry.commentText = c
			entry.save()
			return HttpResponse('Comment Updated Successfully', status=201)

		except Comment.DoesNotExist, e:
			return HttpResponse("Comment Not Found. Therefore cannot be updated", status=400)
		except Exception as e:
			return HttpResponse('Provide commentId in the url, and new comment in comment attribute.', status=400)

class Statistics(View):
	def get(self, request):
		str = '' #Define this to be sent via HttpResponse
		
		# Get Task with Max Comments
		commentDict = Comment.objects.values('taskId').annotate(total=Count('taskId')).order_by('-total')
		task = Task.objects.get(taskId = commentDict[0].get('taskId'))
		str = ('The Task with maximum comments\
				 is = <b>%s</b> with %d Comments'\
				 %(task.title, commentDict[0].get('total')))

		# Get User with Maximum Tasks given that task is Not Deleted by the User
		taskDict = Task.objects.filter(isDeleted = False).values('createdBy').annotate(total=Count('createdBy')).order_by('-total')
		user = User.objects.get(userId = taskDict[0].get('createdBy'))
		str = str + ('</br></br>The User posting maximum\
		 			task is = <b>%s</b> with %d Tasks' 
		 			%(user.username, taskDict[0].get('total')))
		
		# Get User with Maximum Comments given that task is Not Deleted by the User
		task = Task.objects.filter(isDeleted = False)
		taskIds = []	#Create list of Not Deleted Task Id's
		for t in task:
			taskIds.append(t.taskId)

				# Get those comments whose task Id is Not deleted
		commentDict = Comment.objects.filter(taskId__in=taskIds).values('createdBy').annotate(total=Count('createdBy')).order_by('-total')
		user = User.objects.get(userId = commentDict[0].get('createdBy'))
		str = str + ('</br></br>The User posting maximum\
		 			comments is = <b>%s</b> with %d Comments' 
		 			%(user.username, commentDict[0].get('total')))
		

		return HttpResponse(str, status=200)