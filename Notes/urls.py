# Core Django Imports
from django.conf.urls import include, url

# Import from Project Apps
from views import Pages

urlpatterns = [
    url(r'^index/', Pages.as_view()),
]