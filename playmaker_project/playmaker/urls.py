__author__ = 'Vlad Schnakovszki'
import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^' + '$', views.mainpage, name='mainpage'),
    url(r'^' + 'accept-offer/$', views.accept_offer, name='accept_offer'),
    url(r'^' + 'create/$', views.create_session, name='create_session'),
    url(r'^' + 'login/$', views.attempt_login, name='attempt_login'),
    url(r'^' + 'logout/$', views.attempt_logout, name='attempt_logout'),
    url(r'^' + 'make-offer/$', views.make_offer, name='make_offer'),
    url(r'^' + 'register/$', views.register, name='register'),
    url(r'^' + 'bookings/$', views.bookings, name='bookings'),
    url(r'^' + 'preferences/$', views.preferences, name='preferences'),
    url(r'^' + 'profile/(?P<username>[\w\-]+)/$', views.user_profile, name='user_profile'),
    url(r'^' + 'session/(?P<session_id>[\w\-]+)/$', views.view_session_by_id, name='view_session_by_id'),
    url(r'^' + 'sessions/(?P<session_sport>[\w\-]+)/$', views.view_sessions_by_sport, name='view_sessions_by_sport'),
    url(r'^' + 'sessions/city/(?P<session_city>[\w\-]+)/$', views.view_sessions_by_city, name='view_sessions_by_city'),
    url(r'^' + 'sendmsg/$', views.add_message_to_session, name='add_message_to_session'),
    url(r'^' + 'getmsgs/(?P<session_id>[\w\-]+)/$', views.get_messages, name='get_messages'),
    url(r'^' + 'cancel-session/$', views.cancel_session, name='cancel_session'),
    url(r'^' + 'withdraw-offer/$', views.withdraw_offer, name='withdraw_offer'),
)
