from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import *
from django.db.models import Count
from models import *
from forms import RegistrationForm
from forms import AddMessageToSessionForm
from forms import CreateSession
from django.contrib.auth import authenticate
import datetime
from helpers import get_context_dictionary

# Create your views here.
@csrf_exempt
def mainpage(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        sports = Sport.objects.all()
        city = UserPreferredCities.objects.get(user=request.user)
        today = datetime.datetime.now().date()
        sessions = Session.objects.filter(city=city.city, date__gte=today)
        sessions=sessions.annotate(num_offers=Count('offer'))
        sessions = sessions.order_by('date', 'time')
        context_dict = get_context_dictionary(request)
        context_dict['city'] = city
        context_dict['sports'] = sports
        context_dict['sessions'] = sessions
        return render_to_response('mainpage_logged_in.html', context_dict, context)
    else:
        # Show the city selection page if not authenticated.
        cities = []
        all_cities = City.objects.all().order_by('city')
        for city in all_cities:
            cities.append(city.city)
        context_dict = get_context_dictionary(request)
        context_dict['cities'] = cities
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
    context_dict = get_context_dictionary(request)
    context_dict['result'] = failure_reason
    return render_to_response('login_failed.html', context_dict, context, )

@csrf_exempt
def register(request):
    context = RequestContext(request)

    # check if the request contains POST data
    # this happens when a user submits a form
    if request.POST:
        #create form object
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            #hash password with the set_password method
            user.set_password(user.password)
            user.save()
            # return response and redirect user to Bookings page
            return HttpResponseRedirect('bookings.html', context)

    # Show the city selection page if not authenticated.
    cities = []
    all_cities = City.objects.all().order_by('city')
    for city in all_cities:
        cities.append(city.city)
    context_dict = get_context_dictionary(request)
    context_dict['cities'] = cities
    return render_to_response('register.html', context_dict, context)



@csrf_exempt
def bookings(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        context_dict = get_context_dictionary(request)
        user = request.user
        sports = Sport.objects.all()
        sessions_i_created = Session.objects \
            .filter(hostplayer = user) \
            .annotate(num_offers=Count('offer'))
        sessions_i_joined = Session.objects \
            .filter(guestplayer = user) \
            .annotate(num_offers=Count('offer'))
        sessions_i_offered = Session.objects \
            .exclude(guestplayer = user) \
            .filter(offer__guest__exact = user) \
            .annotate(num_offers=Count('offer'))
        context_dict['sports'] = sports
        context_dict['sessions_i_created'] = sessions_i_created
        context_dict['sessions_i_joined'] = sessions_i_joined
        context_dict['sessions_i_offered'] = sessions_i_offered
        return render_to_response('bookings.html', context_dict, context)
    else:
        return render_to_response('login.html', context)


@csrf_exempt
def preferences(request):
    context = RequestContext(request)
    if request.GET:
        if request.user.is_authenticated():
            context_dict = get_context_dictionary(request)
            context_dict['username'] = request.user.username
            context_dict['email'] = request.user.email
            context_dict['first_name'] = request.user.first_name
            context_dict['last_name'] = request.user.last_name
            context_dict['city'] = UserPreferredCities.objects.get(username=request.user).city.city
            return render_to_response('preferences.html', context_dict, context)
        #if not authenticated, go to login page
        else:
            return HttpResponseRedirect('login.html')

    return HttpResponse(status=405)


@csrf_exempt
def user_profile(request, username):
    context = RequestContext(request)
    context_dict = get_context_dictionary(request)
    context_dict['your_key'] = 'your_value'
    return render_to_response('user_profile.html', context_dict, context)

@csrf_exempt
def view_sessions(request):
    context = RequestContext(request)
    username = request.user.username
    sessionsCreated = Session.objects.filter(hostplayer=User.objects.get(username=username))
    sessionsApplied = Session.objects.filter(guestplayer=User.objects.get(username=username))
    context_dict = get_context_dictionary(request)
    context_dict['sessionsICreated'] = sessionsCreated
    context_dict['sessionsIApplied'] = sessionsApplied
    return render_to_response('view_sessions.html', context_dict, context)

@csrf_exempt
def view_session_by_id(request, session_id):
    context = RequestContext(request)
    username = request.user.username
    host_viewing = True
    offer_accepted = False
    session = Session.objects.get(id = session_id)
    offers = Offer.objects.select_related().filter(session = session_id)
    offer_count = offers.__len__()
    messages = Message.objects.filter(session = session_id)
    guestplayer = session.guestplayer
    sports = Sport.objects.all()

    if username != session.hostplayer:
        host_viewing = False

    if guestplayer is not None:
        offer_accepted = True
    context_dict = get_context_dictionary(request)
    context_dict['sports'] = sports
    context_dict['current_viewer'] = username
    context_dict['session'] = session
    context_dict['host_viewing'] = host_viewing
    context_dict['messages'] = messages
    context_dict['offers'] = offers
    context_dict['offer_count'] = offer_count
    context_dict['offer_accepted'] = offer_accepted
    return render_to_response('view_session_by_id.html', context_dict, context)

@csrf_exempt
def view_sessions_by_sport(request, session_sport):
    context = RequestContext(request)
    today = datetime.datetime.now().date()
    sessions = Session.objects.filter(sport=Sport.objects.get(sport_slug=session_sport).sport, date__gte=today)
    sessions = sessions.annotate(num_offers=Count('offer'))
    sessions = sessions.order_by('date', 'time')
    sports = Sport.objects.all()
    context_dict = get_context_dictionary(request)
    context_dict['sport'] = session_sport
    context_dict['sports'] = sports
    context_dict['sessions'] = sessions
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

    return HttpResponseNotModified


@csrf_exempt
def attempt_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
