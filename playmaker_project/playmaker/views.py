from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import *
from django.db.models import Count
from models import *
from forms import RegistrationForm
from forms import AddMessageToSessionForm
from forms import PreferencesForm
from forms import CreateSessionForm
from django.contrib.auth import authenticate
import datetime
import json
from helpers import get_context_dictionary

def mainpage(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        sports = Sport.objects.all()
        city = UserPreferredCities.objects.get(user=request.user)
        edit = city.city.__str__().capitalize()
        city = edit
        today = datetime.datetime.now().date()
        sessions = Session.objects.filter(city=city, date__gte=today, guestplayer=None)
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

def register(request):
    context = RequestContext(request)

    # check if the request contains POST data
    # this happens when a user submits a form
    if request.POST:
        print 'is a post'
        #create form object
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            print 'form is valid'
            user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
            #user = form.save()
            print "username is:", user.username
            #user.save()
            #hash password with the set_password method
            user.set_password(form.cleaned_data['password'])
            user.save()

            print 'saved user'
            upc = UserPreferredCities.objects.create(user=user,
                                                     city=City.objects.get(city=form.cleaned_data['city']), )
            upc.save()

            print 'form is saved'
            if authenticate(username=user.username, password=form.cleaned_data['password']) is None:
                print 'could not authenticate'
            # return response and redirect user to Bookings page
            return render_to_response('bookings.html', context)

    # Show the city selection page if not authenticated.
    cities = []
    print "Some shit happened"
    all_cities = City.objects.all().order_by('city')
    for city in all_cities:
        cities.append(city)
    context_dict = get_context_dictionary(request)
    context_dict['cities'] = cities
    return render_to_response('register.html', context_dict, context)

def bookings(request):
    context = RequestContext(request)
    print 'before is authenticated'
    if request.user.is_authenticated():
        print 'user has been authenticated'
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
            .filter(guestplayer = None) \
            .filter(offer__guest__exact = user) \
            .annotate(num_offers=Count('offer'))
        context_dict['sports'] = sports
        context_dict['sessions_i_created'] = sessions_i_created
        context_dict['sessions_i_joined'] = sessions_i_joined
        context_dict['sessions_i_offered'] = sessions_i_offered
        return render_to_response('bookings.html', context_dict, context)
    else:
        return render_to_response('login.html', context)

def preferences(request):
    context = RequestContext(request)
    context_dict = get_context_dictionary(request)
    sports = Sport.objects.all()
    context_dict['sports'] = sports
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
        form = PreferencesForm(data = request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()
            form_initial = {}
            form_initial['email'] = user.email
            form_initial['first_name'] = user.first_name
            form_initial['last_name'] = user.last_name
            form_initial['city'] = UserPreferredCities.objects.get(user=user).city
            context_dict['form'] = PreferencesForm(initial=form_initial)
            context_dict['updated'] = True
            return HttpResponseRedirect('/preferences/')
            #return render_to_response('preferences.html', context_dict, context)
        else:
            form_initial = {}
            form_initial['email'] = request.user.email
            form_initial['first_name'] = request.user.first_name
            form_initial['last_name'] = request.user.last_name
            form_initial['city'] = UserPreferredCities.objects.get(user=request.user).city
            context_dict['form'] = PreferencesForm(initial=form_initial)
            context_dict['updated'] = False
            return render_to_response('preferences.html', context_dict, context)

    form_initial = {}
    form_initial['email'] = request.user.email
    form_initial['first_name'] = request.user.first_name
    form_initial['last_name'] = request.user.last_name
    form_initial['city'] = UserPreferredCities.objects.get(user=request.user).city
    context_dict['form'] = PreferencesForm(initial=form_initial)
    return render_to_response('preferences.html', context_dict, context)

def user_profile(request, username):
    context = RequestContext(request)
    context_dict = get_context_dictionary(request)
    sports = Sport.objects.all()
    context_dict['sports'] = sports
    users = User.objects.filter(username=username)
    if users.exists():
        user = users[0]
        context_dict['profile_username'] = user.username
        context_dict['first_name'] = user.first_name
        context_dict['last_name'] = user.last_name
        context_dict['city'] = UserPreferredCities.objects.get(user=user).city
    return render_to_response('user_profile.html', context_dict, context)

def view_session_by_id(request, session_id):
    context = RequestContext(request)
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # Ensure the session exists. If not, redirect to sessions list.
    if Session.objects.filter(id = session_id).count() == 0:
        return HttpResponseRedirect('/')

    # Get parameters.
    session = Session.objects.get(id = session_id)
    username = request.user.username
    host_viewing = True
    offer_accepted = False

    context_dict = get_context_dictionary(request)

    # Fetch the offer status. Will be null with count 0 if the user is not the host.
    offers = None
    context_dict['joined'] = False
    offer_count = Offer.objects.filter(session=Session.objects.get(id=session_id)).count()
    if offer_count > 0:
        offers = Offer.objects.filter(session=Session.objects.get(id=session_id))
        context_dict['joined'] = offers.filter(guest=request.user).exists()
    messages = Message.objects.filter(session=Session.objects.get(id=session_id))
    guestplayer = session.guestplayer
    sports = Sport.objects.all()

    if username != session.hostplayer.username:
        host_viewing = False

    if guestplayer is not None:
        if (not host_viewing) and (guestplayer.username != username):
            #it's private
            return HttpResponseRedirect('/')
        offer_accepted = True

    # Add the parameters to the context dictionary and render it.)
    context_dict['sports'] = sports
    context_dict['current_viewer'] = username
    context_dict['session'] = session
    context_dict['host_viewing'] = host_viewing
    context_dict['messages'] = messages
    context_dict['offers'] = offers
    context_dict['offer_count'] = offer_count
    context_dict['offer_accepted'] = offer_accepted
    return render_to_response('view_session_by_id.html', context_dict, context)

def view_sessions_by_sport(request, session_sport):
    context = RequestContext(request)
    today = datetime.datetime.now().date()
    sessions = Session.objects.filter(sport=Sport.objects.get(sport_slug=session_sport).sport, date__gte=today, guestplayer=None)
    sessions = sessions.annotate(num_offers=Count('offer'))
    sessions = sessions.order_by('date', 'time')
    sports = Sport.objects.all()
    context_dict = get_context_dictionary(request)
    context_dict['sport'] = session_sport
    context_dict['sports'] = sports
    context_dict['sessions'] = sessions
    return render_to_response('view_sessions_by_sport.html', context_dict, context)

def view_sessions_by_city(request, session_city):
    context = RequestContext(request)
    today = datetime.datetime.now().date()
    sessions = Session.objects.filter(city=session_city, guestplayer=None)
    sessions = sessions.annotate(num_offers=Count('offer'))
    sessions = sessions.order_by('date', 'time')
    sports = Sport.objects.all()
    edit = session_city.capitalize()
    session_city = edit
    context_dict = get_context_dictionary(request)
    context_dict['city'] = session_city
    context_dict['sports'] = sports
    context_dict['sessions'] = sessions
    return render_to_response('view_sessions_by_city.html', context_dict, context)

def add_message_to_session(request):
    # Only accept POST requests. Return an error if not, since this is an AJAX call.
    if not request.POST:
        print "Not a POST"
        return HttpResponse("Not a POST", status=400)
    # Make sure the user is valid. Return an error if not, since this is an AJAX call.
    if not request.user.is_authenticated() or not request.user.is_active:
        print "Not logged in"
        return HttpResponse("Not logged in", status=400)
    form = AddMessageToSessionForm(request.POST)
    if not form.is_valid():
        print "Form error"
        print form.errors
        return HttpResponse("Form error", status=400)

    session = Session.objects.get(id=form.cleaned_data['session_id'])

    # Determine if the message is public or private.
    # If private, determine who should be able to view it.
    viewer = None
    print session.guestplayer
    if session.guestplayer is not None:
        if session.hostplayer is request.user:
            viewer = session.guestplayer
        elif session.guestplayer is request.user:
            viewer = session.hostplayer
        else: # Not host or guest in private session, refuse.
            print "Access denied"
            return HttpResponse("Access denied", status=400)

    # Store the message to the database.
    message = Message.objects.create(session=session, user_op=request.user, user_viewer=viewer,
                                     date=datetime.datetime.now(), time=datetime.datetime.now(), message=form.cleaned_data['message'])
    message.save()

    # Confirm addition.
    return HttpResponse(status=200)

def get_messages(request, session_id):
    response = []
    messages_all = Message.objects.filter(session=session_id)
    messages_public = messages_all.filter(user_viewer=None)
    messages_private = messages_all.filter(user_viewer=request.user)
    messages_filtered = (messages_public | messages_private).order_by('date', 'time')
    for message in messages_filtered:
        viewer = message.user_viewer
        if viewer is not None:
            viewer = str(viewer)
        response.append({
            'user_op': str(message.user_op),
            'user_viewer': viewer,
            'date': str(message.date),
            'time': str(message.time),
            'message': message.message,
        })
    return HttpResponse(json.dumps(response, indent=4))

def create_session(request):
    context = RequestContext(request)
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # Create the session if the method is POST.
    if request.POST:
        form = CreateSessionForm(data = request.POST)
        if form.is_valid():
            # Create session object.
            session = Session.objects.create(sport=Sport.objects.get(sport = request.POST['sport']), hostplayer = request.user, guestplayer = None,
                                             date = request.POST['date'], time = request.POST['time'], city = City.objects.get(city=request.POST['city']),
                                             location = request.POST['location'], price = request.POST['price'], details = request.POST.get('details', ""))
            session.save()
            return HttpResponseRedirect("/session/" + str(session.id) + "/")
        else:
            # Display the page if the method is GET.
            print form.errors
            context_dict = get_context_dictionary(request)
            sports = Sport.objects.all()
            cities = City.objects.all().order_by('city')
            user_preferred_city = UserPreferredCities.objects.get(user=request.user)
            context_dict['sports'] = sports
            context_dict['cities'] = cities
            context_dict['user_preferred_city'] = user_preferred_city
            context['session_created'] =False
            return render_to_response('create_session.html', context_dict, context)

    # Display the page if the method is GET.
    context_dict = get_context_dictionary(request)
    sports = Sport.objects.all()
    cities = City.objects.all().order_by('city')
    user_preferred_city = UserPreferredCities.objects.get(user=request.user)
    context_dict['sports'] = sports
    context_dict['cities'] = cities
    context_dict['user_preferred_city'] = user_preferred_city
    return render_to_response('create_session.html', context_dict, context)

def make_offer(request):
    context = RequestContext(request)
    # Only accept POST requests. Redirect to main if not.
    if not request.POST:
        return HttpResponseRedirect('/')
    # Make sure the user is valid. Redirect to login page if not logged in.
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # Fetch the session. Return 400 if invalid.
    session_id = request.POST['session']
    if session_id is None:
        return HttpResponseRedirect('/')
    session = Session.objects.get(id=session_id)
    if session is None:
        return HttpResponseRedirect('/')

    # Check that the user has not made an offer for this session before. Return 409 if he did.
    if Offer.objects.filter(session=session, guest=request.user).count() is not 0:
        context_dict = get_context_dictionary(request)
        context_dict['result'] = 'You have already posted an offer for this session!'
        return render_to_response('view_session_by_id.html', context_dict, context)

    # Save the offer.
    Offer.objects.create(session=session, guest=request.user).save()
    # Show the confirmation page.
    context_dict = get_context_dictionary(request)
    context_dict['result'] = 'Your offer has been placed!'

    return render_to_response('view_session_by_id.html', context_dict, context)

def accept_offer(request):
    context = RequestContext(request)
    # Only accept POST requests. Redirect to main if not.
    if not request.POST:
        return HttpResponseRedirect('/')
    # Make sure the user is valid. Redirect to login page if not logged in.
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # If no offer id submitted, redirect to sessions page.
    offer_id = request.POST['offer']
    if offer_id is None:
        return HttpResponseRedirect('/')

    # If the user is not the op, this is very likely a hack attempt.
    # Take revenge by redirecting to main page.
    offer = Offer.objects.get(id=offer_id)
    if request.user != offer.session.hostplayer:
        return HttpResponseRedirect('/')

    offer.session.guestplayer = offer.guest
    offer.session.save()

    # Reload the page.
    return render_to_response('view_session_by_id.html', context)

def cancel_session(request):
    # Only accept POST requests. Redirect to main if not.
    if not request.POST:
        return HttpResponseRedirect('/')
    # Make sure the user is valid. Redirect to login page if not logged in.
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # Fetch the session. Return 400 if invalid.
    session_id = request.POST['session']
    if session_id is None:
        return HttpResponseRedirect('/')
    session = Session.objects.get(id=session_id)
    if session is None:
        return HttpResponseRedirect('/')

    # If the user is not the host, this is very likely a hack attempt.
    # Take revenge by redirecting to main page.
    if request.user != session.hostplayer:
        return HttpResponseRedirect('/')

    # Remove the offers.
    Offer.objects.filter(session=session).delete()

    # Remove the session.
    session.delete()

    return HttpResponseRedirect('/')

def withdraw_offer(request):
    # Only accept POST requests. Redirect to main if not.
    if not request.POST:
        return HttpResponseRedirect('/')
    # Make sure the user is valid. Redirect to login page if not logged in.
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect('/login/')

    # Fetch the session. Return 400 if invalid.
    session_id = request.POST['session']
    if session_id is None:
        return HttpResponseRedirect('/')
    session = Session.objects.get(id=session_id)
    if session is None:
        return HttpResponseRedirect('/')

    # Get the offer. If null, reload the page.
    offer = Offer.objects.get(session=session, guest=request.user)
    if offer is None:
        return HttpResponseRedirect('/session/' + str(session.id) + '/')

    # Remove the guest from the session.
    session.guestplayer = None
    session.save()

    # Remove the offer.
    offer.delete()
    print 'deleted offer'
    # Reload the page.
    return HttpResponseRedirect('/session/' + str(session.id) + '/')

def attempt_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
