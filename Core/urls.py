from django.conf.urls import url
from . import views

urlpatterns = [

    # Authentication URL
    url(r'^login/$', views.Login, name="Login"),
    url(r'^logout/$', views.Logout, name="Logout"),

]
