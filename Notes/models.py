from django.db import models

# Create your models here.
class Task(models.Model):
	LABEL_LIST = (
        ('1', 'Todo'),
        ('2', 'Doing'),
        ('3', 'Done'),
    )
	COLOURS = (
		('#808080','Gray'),
		('#000000','Black'),
		('#FF0000','Red'),
		('#0000FF','Blue')
	)	

	# CANNOT BE BLANK = Title. Label. CreatedBy. DueDate
	# CAN BE BLANK = Description. Color. Comments
	taskId = models.AutoField(primary_key=True)
	title = models.CharField(max_length = 30, blank=False)
	description = models.CharField(max_length = 100, blank=True)
	label = models.CharField(max_length=1, choices=LABEL_LIST, blank=False)
	color = models.CharField(max_length=7, choices=COLOURS, blank=True) #STORE A HEX FIELD.
	comments = models.CharField(max_length=255, blank=True)
	createdBy = models.CharField(max_length=10, blank=False)
	dueDate = models.DateField(null=False)

	# def __str__(self):
	# 	return ('DUE DATE = %s</br>\
	# 			TITLE = %s</br>\
	# 			DESCRIPTION = %s</br>\
	# 			AUTHOR = %s</br>\
	# 			</br></br>'
	# 			% (self.dueDate, self.title, self.description, self.createdBy))

	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		ordering = ["dueDate"]

	# class Admin:
	# 	pass


# If blank=True then the field will not be required, whereas if it's False the field cannot be blank.
# The exception is CharFields and TextFields, which in Django are never saved as NULL. Blank values are stored in the DB as an empty string ('')
# CHAR and TEXT types are never saved as NULL by Django, so null=True is unnecessary. 

class Comment(models.Model):
	commentId = models.AutoField(primary_key=True)
	taskId = models.ForeignKey(Task, null=False, blank=False)
	createdOn = models.DateTimeField(auto_now_add=True)
	UpdatedOn = models.DateTimeField(auto_now_add=True)
	createdBy = models.CharField(max_length=10, blank=False) #CANNOT be blank.
	commentText = models.CharField(max_length=100, blank=False)

	def __str__(self):
		return '%s' % (self.commentText)

	class Meta:
		ordering = ["createdBy"]

	# class Admin:
	# 	pass

# The following APIs need to be implemented:
# - Get all tasks grouped by list (GET / tasks/)
# - Create a task (POST /tasks/)
# - Get the task details (GET /tasks/<task_id>/)
# - Edit a task (PUT /tasks/<task_id>/)
# - Delete a task (DELETE /tasks/<task_id>/)
# - Add / edit a comment