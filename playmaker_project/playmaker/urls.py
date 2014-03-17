__author__ = 'Vlad Schnakovszki'
import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^' + '$', views.mainpage, name='mainpage'),
    url(r'^' + 'login/$', views.attempt_login, name='attempt_login'),
    url(r'^' + 'register/$', views.register, name='register'),
    url(r'^' + 'bookings/$', views.bookings, name='bookings'),
    url(r'^' + 'preferences/$', views.preferences, name='preferences'),
    url(r'^' + 'profile/(?P<username>[\w\-]+)/$', views.user_profile, name='user_profile'),
    url(r'^' + 'session/(?P<session_id>[\w\-]+)/$', views.view_session_by_id, name='view_session_by_id'),
    url(r'^' + 'sessions/$', views.view_sessions, name='view_sessions'),
    url(r'^' + 'sessions/(?P<session_sport>[\w\-]+)/$', views.view_sessions_by_sport, name='view_sessions_by_sport'),
    url(r'^' + 'logout/$', views.attempt_logout, name='attempt_logout'),
    url(r'^' + 'create/$', views.create_session, name='create_session'),
)
