# Core Django Imports
from django.conf.urls import include, url

from views import ip
from views import visionApiFile
from views import visionApiScript

urlpatterns = [
    url(r'^ip', ip),
    url(r'^vision/file', visionApiFile),
    url(r'^vision/script', visionApiScript),
]