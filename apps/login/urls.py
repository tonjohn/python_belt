from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^process$', views.process, name="process"),
	url(r'^login', views.login, name="login"),
	url(r'^register', views.do_register, name="register"),
	url(r'^success$', views.success, name="success"),
	url(r'^logout$', views.logout, name="logout"),
	url(r'^user/(?P<userid>\d+)?$', views.view_user, name="view_user"),
]
