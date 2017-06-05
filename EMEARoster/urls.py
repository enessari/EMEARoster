from django.conf.urls import include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Core.urls')),
    url(r'^', include('Scheduler.urls')),
    url('', include('social_django.urls', namespace='social')),
]

# Change admin site title
admin.site.site_header = _("EMEA Roster Administration")
admin.site.site_title = _("EMEA Roster")