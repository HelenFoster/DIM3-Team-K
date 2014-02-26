import os
from dateutil.parser import parse

def add_city(city):
    print "City: " + city
    City.objects.get_or_create(city=city)

def add_cities(cities):
    for city in cities:
        add_city(city)

def add_sport(sport):
    print "Sport: " + sport
    Sport.objects.get_or_create(sport=sport)

def add_sports(sports):
    for sport in sports:
        add_sport(sport)

def add_user(username, email, firstname, lastname):
    print "User: " + username
    user = User.objects.create_user(username, email, password=username)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

def add_superuser(username, email, firstname, lastname):
    print "Super user: " + username
    user = User.objects.create_superuser(username, email, password=username)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

def add_session(sport, hostplayer, guestplayer, date, time, city, location, price, details):
    if guestplayer is not None:
        guestplayer = User.objects.get(username=guestplayer)

    Session.objects.get_or_create(
        sport = Sport.objects.get(sport=sport),
        hostplayer = User.objects.get(username=hostplayer),
        guestplayer = guestplayer,
        date = parse(date),
        time = parse(time),
        city = City.objects.get(city=city),
        location = location,
        price = price,
        details = details,
    )

def add_user_preferred_city(user, city):
    UserPreferredCities.objects.get_or_create(
        user = User.objects.get(username = user),
        city = City.objects.get(city = city),
    )

def add_offer(session, guest):
    Offer.objects.get_or_create(
        session = Session.objects.get(id=session),
        guest = User.objects.get(username=guest),
    )

def add_message(session, user_op, user_viewer, date, time, message):
    if user_viewer is not None:
        user_viewer = User.objects.get(username=user_viewer)
    Message.objects.get_or_create(
        session = Session.objects.get(id=session),
        user_op = User.objects.get(username=user_op),
        user_viewer = user_viewer,
        date = parse(date),
        time = parse(time),
        message = message,
    )

def populate():
    add_cities(["Glasgow", "Edinburgh", "London", "Aberdeen", "Carlisle", "Leeds", "York", "Manchester", "Birmingham", "Essex", "Southampton", "Norwich", "Doncaster", ])
    add_sports(["Squash", "Tennis", "Chess", "Badminton", "Pool", ])

    # Superusers.
    add_superuser("admin", "admin@playmaker.com", "Admin", "Nimda")

    # Users.
    add_user("jack", "jack@jones.com", "Jack", "Jones")
    add_user("john", "john@doe.com", "John", "Doe")
    add_user("leif", "leif@azzopardi.com", "Leif", "Azzopardi")
    add_user("martynas", "martynas@buivys.com", "Martynas", "Buivys")
    add_user("raluca", "raluca@criste.com", "Raluca", "Criste")
    add_user("helen", "helen@foster.com", "Helen", "Foster")
    add_user("tomasz", "tomasz@sadowski.com", "Tomasz", "Sadowski")
    add_user("vlad", "vlad@schnakovszki.com", "Vlad", "Schnakovszki")

    # Add favorite cities.
    add_user_preferred_city("jack", "London")
    add_user_preferred_city("john", "Aberdeen")
    add_user_preferred_city("leif", "Glasgow")
    add_user_preferred_city("helen", "Glasgow")
    add_user_preferred_city("vlad", "Glasgow")

    # Sessions.
    add_session("Squash", "vlad", None, "2014-03-01", "18:45", "Glasgow", "Stevenson Court 2", 0.65, "Bring your own racquet!")

    # Offers.
    add_offer(1, "john")
    add_offer(1, "martynas")
    add_offer(1, "tomasz")

    # Messages.
    add_message(1, "john", None, "2014-02-19", "18:21", "Hey mate, can you do 20:00?")
    add_message(1, "martynas", None, "2014-02-21", "19:13", "Do you have a racquet I could borrow?")
    add_message(1, "vlad", None, "2014-02-20", "12:21", "@john, naah, sorry, gotta be somewhere else by then...")
    add_message(1, "vlad", None, "2014-02-20", "16.33", "@martynas, you can borrow one from the desk, it's 1 pound.")


# Start execution here!
if __name__ ==  '__main__':
    print "Starting PlayMaker population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playmaker_project.settings')
    from django.contrib.auth.models import User
    from playmaker.models import *
    populate()
