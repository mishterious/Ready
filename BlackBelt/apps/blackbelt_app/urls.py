
from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^success$', views.success)     # This line has changed!
]