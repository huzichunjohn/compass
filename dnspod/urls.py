from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^(?P<domain_id>[0-9]+)/$', views.get_records_by_domain_id, name="record_list"),
    url(r'^(?P<domain_id>[0-9]+)/records/(?P<record_id>[0-9]+)/edit/', views.edit_record, name="edit_record"),
    url(r'^(?P<domain_id>[0-9]+)/records/(?P<record_id>[0-9]+)/delete/', views.delete_record, name="delete_record"),
    url(r'^', views.index, name="index"),
]
