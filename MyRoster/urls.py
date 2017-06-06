from django.conf.urls import url
from . import views

urlpatterns = [

    # MyRoster URL..
    url(r'^myroster_rows/$', views.myroster_rows, name="myroster_rows"),

]
