from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Core.urls')),
    url(r'^', include('Scheduler.urls')),
    url('', include('social_django.urls', namespace='social')),
]
