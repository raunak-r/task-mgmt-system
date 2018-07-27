# Core Django Imports
from django.conf.urls import include, url

# Import from Project Apps
from views import Pages
urlpatterns = [
    url(r'^index/', Pages.as_view()),
]

from views import Users
from views import Tasks
from views import Comments
from views import Statistics


urlpatterns += [
	url(r'^tasks', Tasks.as_view()),
	url(r'^comments', Comments.as_view()),
	url(r'^stats', Statistics.as_view()),
]

# from django.views.generic import TemplateView
# urlpatterns += [
#     url(r'^users/post$', TemplateView.as_view(template_name='users/usersPost.html')),
# ]

urlpatterns += [
	# url(r'^users/([a-z]{1,4})', Users.as_view()),
	url(r'^users', Users.as_view()),
]