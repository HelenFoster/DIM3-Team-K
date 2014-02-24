__author__ = 'Vlad Schnakovszki'
import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^' + 'login/$', views.login, name='login'),
    url(r'^' + 'register/$', views.register, name='register'),
    url(r'^' + 'bookings/$', views.bookings, name='bookings'),
    url(r'^' + 'preferences/$', views.preferences, name='preferences'),
    url(r'^' + 'profile/(?P<username>[\w\-]+)/$', views.user_profile, name='user_profile'),
    url(r'^' + 'sessions/$', views.view_sessions, name='view_sessions'),
    url(r'^' + 'sessions/(?P<session_id>[\w\-]+)/$', views.view_session_by_id, name='view_session_by_id'),
    url(r'^' + 'sessions/(?P<session_sport>[\w\-]+)/$', views.view_sessions_by_sport, name='view_sessions_by_sport'),
)