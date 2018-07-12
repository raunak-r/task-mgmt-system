from django.contrib import admin

# Register your models here.

# USERNAME = 'raunak'
# p/w = 'happay'

from models import Task
from models import Comment

admin.site.register(Task)
admin.site.register(Comment)