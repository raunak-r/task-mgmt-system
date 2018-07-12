from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# Import from Project Apps
urlpatterns += [
    url(r'^tasks/', include('Notes.urls')),
]