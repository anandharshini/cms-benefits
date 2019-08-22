from django.conf.urls import url
from . import views

urlpatterns = [
    url('^', views.broker_home_view, name='broker_home_view',),
]