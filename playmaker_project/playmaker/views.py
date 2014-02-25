from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *


# Create your views here.

@csrf_exempt
def login(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('login.html', context_dict, context)

@csrf_exempt
def register(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('register.html', context_dict, context)

@csrf_exempt
def bookings(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('bookings.html', context_dict, context)

@csrf_exempt
def preferences(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('preferences.html', context_dict, context)

@csrf_exempt
def user_profile(request, username):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('user_profile.html', context_dict, context)

@csrf_exempt
def view_sessions(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('view_sessions.html', context_dict, context)

@csrf_exempt
def view_session_by_id(request, session_id):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('view_session_by_id.html', context_dict, context)

@csrf_exempt
def view_sessions_by_sport(request, session_sport):
    print session_sport
    context = RequestContext(request)
    session_list = Session.objects.filter(sport=session_sport)
    print len(session_list)
    context_dict = {'sport': session_sport, 'sessions': session_list}
    return render_to_response('view_sessions_by_sport.html', context_dict, context)
