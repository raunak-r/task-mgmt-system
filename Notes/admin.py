from django.contrib import admin

# Register your models here.

# USERNAME = 'raunak'
# p/w = 'happay'

from models import Task
from models import Comment
from models import User

class TaskModelAdmin(admin.ModelAdmin):
	list_display = ['taskId', 'title', 'description', 'label', 'color', 'comments', 'createdBy', 'dueDate']
	
	# Same attribute cannot be in both display_links and editable.
	list_display_links = ['title']
	list_editable = ['description', 'comments']

	# To show Filters on the side bar
	list_filter = ['createdBy', 'dueDate', ('isDeleted', admin.BooleanFieldListFilter)]	
	
	list_per_page = 20	#Number of entries to show on each page

	class Meta:
		model = Task

class CommentModelAdmin(admin.ModelAdmin):
	list_display = ['commentId', 'commentText', 'createdOn', 'UpdatedOn', 'createdBy', 'taskId_id']
	
	# Show Filters on the side bar and list only those Tasks which are referenced by the Foreign Key in Comments Table.
	list_filter = (
		('taskId', admin.RelatedOnlyFieldListFilter),
		('createdBy', admin.RelatedOnlyFieldListFilter),
	)

	class Meta:
		model = Comment

class UserModelAdmin(admin.ModelAdmin):
	list_display = ['userId', 'username', 'createdOn']
	list_editable = ['userId', 'username']
	list_filter = [('isActive', admin.BooleanFieldListFilter)]

	class Meta:
		model = User

admin.site.register(Task, TaskModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(User, UserModelAdmin)