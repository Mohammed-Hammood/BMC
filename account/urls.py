from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'account_app'

urlpatterns = [
    url(r'^uploaders/$', views.uploaders_view, name='uploaders'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^settings/$', views.account_edit, name='account-edit'),
    url(r'^account-delete$', views.account_delete, name='account-delete'),
    url(r'^password-change$', views.password_change, name='password-change'),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^register/$', views.RegistrationView.as_view(), name="register"),
    url(r'^(?P<username>[-\w]+)$', views.ProfileView.as_view(), name='profile'),

    # url(r'^account-edit/$', views.user_info_change, name='account-edit'),
    # url(r'^password-change/$', views.password_change, name='password-change'),

]
