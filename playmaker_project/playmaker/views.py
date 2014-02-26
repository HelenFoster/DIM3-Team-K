from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from models import *


# Create your views here.
@csrf_exempt
def mainpage(request):
    context = RequestContext(request)
    # Show the city selection page if not authenticated.
    # if not request.user.is_authenticated():
    # Load the animals to the dictionary.
    cities = []
    all_cities = City.objects.all().order_by('city')
    for city in all_cities:
        print city.city
        cities.append(
            city.city
        )
    context_dict = {'cities': cities, }
    return render_to_response('mainpage.html', context_dict, context)


# To be called when the user clicks the login button.
# Will attempt to authenticate the user.
# If the credentials are valid, redirect to the main page, where the user should now see the activities.
# If the credentials are invalid, render the login_failed page with the proper failure reason.
@csrf_protect
def login(request):
    context = RequestContext(request)
    failure_reason = 'OK'
    # Only accept POST requests.
    if request.POST:
        # Extract the username and password from the request.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Valid user, credentials stored, go to main page.
                login(request, user)
                return HttpResponseRedirect('mainpage.html', context)
            else:
                failure_reason = 'Your account is disabled!'
        else:
            failure_reason = 'Invalid credentials!'
    else:
        failure_reason = 'Invalid request method!'
    # Add the failure_reason and render the login_failed page.
    context_dict = {'result': failure_reason}
    return render_to_response('login_failed.html', context_dict, context, )

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
