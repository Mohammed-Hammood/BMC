from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'notifications_app'

urlpatterns = [
    path('', views.notifications_list, name='home'),
    url(r'^n-l/$', views.notifications_loader, name="notifications-loader"),
]