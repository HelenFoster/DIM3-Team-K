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

def add_user(username, email, firstname, lastname, city):
    print "User: " + username
    user = User.objects.create_user(username,email, password=username)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
    add_user_preferred_city(username, city)

def add_superuser(username, email, firstname, lastname, city):
    print "Super user: " + username
    user = User.objects.create_superuser(username, email, password=username)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
    add_user_preferred_city(username, city)

#called from user addition functions
def add_user_preferred_city(user, city):
    UserPreferredCities.objects.get_or_create(
        user = User.objects.get(username = user),
        city = City.objects.get(city = city),
    )
    print "Preferred city: %s, %s" % (user, city)

def add_session(id, sport, hostplayer, guestplayer, date, time, city, location, price, details):
    print "Session [%d]: %s, %s %s" % (id, hostplayer, date, time)
    if guestplayer is not None:
        guestplayer = User.objects.get(username=guestplayer)
    Session.objects.get_or_create(
        id = id,
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

def add_offer(session, guest):
    offer = Offer.objects.get_or_create(
        session = Session.objects.get(id=session),
        guest = User.objects.get(username=guest),
    )[0]
    print "Offer [%d]: %d, %s" % (offer.id, session, guest)

def add_message(session, user_op, user_viewer, date, time, message):
    if user_viewer is not None:
        user_viewer = User.objects.get(username=user_viewer)
    msg = Message.objects.get_or_create(
        session = Session.objects.get(id=session),
        user_op = User.objects.get(username=user_op),
        user_viewer = user_viewer,
        date = parse(date),
        time = parse(time),
        message = message,
    )[0]
    print "Message [%d]: %s" % (msg.id, message)

def populate():
    #Delete all rows, so we don't need to delete the database and rerun syncdb unless we changed the models.
    Message.objects.all().delete()
    Offer.objects.all().delete()
    UserPreferredCities.objects.all().delete()
    Session.objects.all().delete()
    Sport.objects.all().delete()
    City.objects.all().delete()
    User.objects.all().delete()

    add_cities(["Glasgow", "Edinburgh", "London", "Aberdeen", "Carlisle", "Leeds", "York", "Manchester", "Birmingham", "Essex", "Southampton", "Norwich", "Doncaster", ])
    add_sports(["Squash", "Tennis", "Chess", "Badminton", "Pool", ])

    # Superusers.
    add_superuser("admin", "admin@playmaker.com", "Admin", "Nimda", "Edinburgh")

    # Users.
    add_user("jack", "jack@jones.com", "Jack", "Jones", "London")
    add_user("john", "john@doe.com", "John", "Doe", "Aberdeen")
    add_user("leif", "leif@azzopardi.com", "Leif", "Azzopardi", "Glasgow")
    add_user("martynas", "martynas@buivys.com", "Martynas", "Buivys", "Glasgow")
    add_user("raluca", "raluca@criste.com", "Raluca", "Criste", "Glasgow")
    add_user("helen", "helen@foster.com", "Helen", "Foster", "Glasgow")
    add_user("tomasz", "tomasz@sadowski.com", "Tomasz", "Sadowski", "Glasgow")
    add_user("vlad", "vlad@schnakovszki.com", "Vlad", "Schnakovszki", "Glasgow")

    # Sessions.
    #add_session(id, sport, hostplayer, guestplayer, date, time, city, location, price, details)
    add_session(1, "Squash", "vlad", "raluca", "2015-03-11", "18:45", "Glasgow", "Stevenson Court 2", 0.65, "Bring your own racquet!")
    add_session(2, "Tennis", "tomasz", None, "2015-03-12", "19:00", "Glasgow", "Stevenson Court 2", 0.65, "")
    add_session(3, "Tennis", "helen", None, "2015-03-13", "19:30", "Glasgow", "Stevenson Court 2", 0.65, "")

    # Offers.
    add_offer(1, "john")
    add_offer(1, "martynas")
    add_offer(1, "tomasz")
    add_offer(2, "jack")
    add_offer(2, "leif")

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
