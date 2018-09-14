# Core Django Imports
from django.conf.urls import include, url

from views import ip

urlpatterns = [
    url(r'^ip', ip),
]