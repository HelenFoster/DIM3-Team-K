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

def add_member(username, email, firstname, lastname):
    print "Member: " + username
    Member.objects.get_or_create(
        username = username,
        email = email,
        firstname = firstname,
        lastname = lastname,
    )

def add_session(sport, hostplayer, guestplayer, date, time, city, location, price, details):
    if guestplayer is not None:
        guestplayer = Member.objects.get(username=guestplayer)
    Session.objects.get_or_create(
        sport = Sport.objects.get(sport=sport),
        hostplayer = Member.objects.get(username=hostplayer),
        guestplayer = guestplayer,
        date = parse(date),
        time = parse(time),
        city = City.objects.get(city=city),
        location = location,
        price = price,
        details = details,
    )

def add_offer(session, guest):
    Offer.objects.get_or_create(
        session = Session.objects.get(id=session),
        guest = Member.objects.get(username=guest),
    )

def add_message(session, user_op, user_viewer, date, time, message):
    if user_viewer is not None:
        user_viewer = Member.objects.get(username=user_viewer)
    Message.objects.get_or_create(
        session = Session.objects.get(id=session),
        user_op = Member.objects.get(username=user_op),
        user_viewer = user_viewer,
        date = parse(date),
        time = parse(time),
        message = message,
    )

def populate():
    add_cities(["Glasgow", "Edinburgh", "London", "Aberdeen", "Carlisle", "Leeds", "York", "Manchester", "Birmingham", "Essex", "Southampton", "Norwich", "Doncaster", ])
    add_sports(["Squash", "Tennis", "Chess", "Badminton", "Pool", ])
    
    # Members.
    add_member("jack", "jack@jones.com", "Jack", "Jones")
    add_member("john", "john@doe.com", "John", "Doe")
    add_member("leif", "leif@azzopardi.com", "Leif", "Azzopardi")
    add_member("martynas", "martynas@buivys.com", "Martynas", "Buivys")
    add_member("raluca", "raluca@criste.com", "Raluca", "Criste")
    add_member("helen", "helen@foster.com", "Helen", "Foster")
    add_member("tomasz", "tomasz@sadowski.com", "Tomasz", "Sadowski")
    add_member("vlad", "vlad@schnakovszki.com", "Vlad", "Schnakovszki")

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
    from playmaker.models import *
    populate()
