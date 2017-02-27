from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^dashboard$', views.index, name="index"),
	url(r'^wish_items/(?P<object_id>\d+)$', views.show, name="view_item"),
	url(r'^wish_items/create$', views.create, name="create_item"),
	url(r'^wish_items/(?P<object_id>\d+)/add$', views.add, name="add_item"),
	url(r'^wish_items/(?P<object_id>\d+)/remove$', views.remove, name="remove_item"),
	url(r'^wish_items/(?P<object_id>\d+)/delete$', views.delete, name="delete_item"),
]
