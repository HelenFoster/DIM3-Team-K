from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login
from django.http import *
from django.db.models import Count
from models import *
from forms import RegistrationForm
from forms import AddMessageToSessionForm
from django.contrib.auth import authenticate


# Create your views here.
@csrf_exempt
def mainpage(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        context_dict = {}
        return render_to_response('mainpage_logged_in.html', context_dict, context)
    else:
        # Show the city selection page if not authenticated.
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
@csrf_exempt
def attempt_login(request):
    context = RequestContext(request)
    failure_reason = 'OK'
    # Display the login page.
    if not request.POST:
        context = RequestContext(request)
        return render_to_response('login.html', context)

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
                return HttpResponseRedirect('/', context)
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
    # only accept POST requests
    if request.POST:
       #create form object
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # return response and redirect user to Bookings page
            return HttpResponseRedirect('bookings.html', context)

    failure_reason = 'Unable to register!'
    # Add the failure_reason and render the login_failed page.
    context_dict = {'result': failure_reason}
    return render_to_response('register.html', context_dict, context)

@csrf_exempt
def bookings(request):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('bookings.html', context_dict, context)

@csrf_exempt
def preferences(request):
    context = RequestContext(request)
    if request.GET:
        if request.user.is_authenticated():
            username = User.objects.get(username=request.user)
            email = User.objects.get(email=request.email)
            first_name = User.objects.get(first_name=request.first_name)
            last_name = User.object.get(last_name=request.last_name)
            city = UserPreferredCities.objects.get(username=username).city
            context_dict = {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name,
                            'city': city}
            return render_to_response('preferences.html', context_dict, context)
        #if not authenticated, go to login page
        else:
            return HttpResponseRedirect('login.html')

    return HttpResponse(status=405)


@csrf_exempt
def user_profile(request, username):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('user_profile.html', context_dict, context)

@csrf_exempt
def view_sessions(request):
    context = RequestContext(request)
    username = request.user.username
    sessionsCreated = Session.objects.filter(hostplayer=User.objects.get(username=username))
    sessionsApplied = Session.objects.filter(guestplayer=User.objects.get(username=username))
    context_dict = {'sessionsICreated': sessionsCreated, 'sessionsIApplied': sessionsApplied}
    return render_to_response('view_sessions.html', context_dict, context)

@csrf_exempt
def view_session_by_id(request, session_id):
    context = RequestContext(request)
    context_dict = {'your_key': 'your_value'}
    return render_to_response('view_session_by_id.html', context_dict, context)

@csrf_exempt
def view_sessions_by_sport(request, session_sport):
    context = RequestContext(request)
    sessions = Session.objects.filter(sport=session_sport).annotate(num_offers=Count('offer'))
    sports = Sport.objects.all()
    context_dict = {'sport': session_sport, 'sports': sports, 'sessions': sessions}
    return render_to_response('view_sessions_by_sport.html', context_dict, context)

@csrf_exempt
def add_message_to_session(request):
    context = RequestContext(request)
    #    only accept POST requests
    if request.POST:
       #    create form object
        form = AddMessageToSessionForm(request.POST)
        #   if form is valid
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse(status=200)
        else:
            #   print the problems to the terminal
            print form.errors
            #   return 405 response
            return HttpResponse(status=405)
    failure_reason = 'Unable to register!'
    #   add the reason of the failure
    context_dict = {'result': failure_reason}
    #   return http response
    return HttpResponseNotModified