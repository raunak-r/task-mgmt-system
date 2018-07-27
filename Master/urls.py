from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# Import from Project Apps
urlpatterns += [
    url(r'^Notes/', include('Notes.urls')),
    url(r'^rest/', include('RestApi.urls')),
]