# Core Django Imports
from django.conf.urls import include, url

from views import ip
from views import visionApi
urlpatterns = [
    url(r'^ip', ip),
    url(r'^vision', visionApi),
]