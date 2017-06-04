from django.conf.urls import url
from . import views

urlpatterns = [

    # Root URL..
    url(r'^$', views.index, name="index"),

    # Get Rows for the roster
    url(r'^get_rows/$', views.get_rows, name="get_rows"),

    # Shuffle Rows
    url(r'^shuffle_rows/$', views.shuffle_rows, name="shuffle_rows"),

    # Shuffle save
    url(r'^shuffle_save/$', views.shuffle_save, name="shuffle_save"),

    # Audit Rows save
    url(r'^audit_rows/$', views.send_audit_rows, name="audit_rows"),

    # Delete audit rows by dates
    url(r'^delete_date_rows/$', views.delete_date_rows, name="delete_date_rows"),

    # Edit Cell rows
    url(r'^update_rows/$', views.updatecell, name="updatecell"),

]
