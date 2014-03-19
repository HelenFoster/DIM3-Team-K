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
    UserProfile.objects.get_or_create(
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
    UserProfile.objects.all().delete()
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
    add_session(1, "Squash", "vlad", "raluca", "2015-03-20", "18:45", "Glasgow", "Stevenson Court 2", 0.65, "Bring your own racquet!")
    add_session(2, "Tennis", "tomasz", None, "2015-03-21", "19:00", "Glasgow", "Stevenson Court 2", 0.65, "")
    add_session(3, "Tennis", "helen", None, "2015-03-25", "19:30", "Glasgow", "Stevenson Court 2", 0.65, "")
    add_session(4, "Squash", "jack", None, "2015-03-20", "18:00", "London", "?", 1.50, "")
    add_session(5, "Chess", "leif", None, "2015-03-20", "19:15", "Glasgow", "Round reading room", 0, "")
    add_session(6, "Chess", "martynas", None, "2015-03-22", "19:15", "Glasgow", "The non existent undergrad common room", 0, "")
    add_session(7, "Chess", "vlad", None, "2015-03-22", "19:15", "Edinburgh", "The non existent undergrad common room", 0, "")
    add_session(8, "Squash", "leif", None, "2015-03-20", "19:15", "Aberdeen", "Level 3 LAB", 0.5, "")
    add_session(9, "Badminton", "leif", None, "2015-03-21", "19:15", "London", "Level1 Lab", 0.5, "")
    add_session(10, "Badminton", "john", None, "2015-03-21", "19:15", "Glasgow", "My Computer studio", 1.05, "")
    add_session(11, "Chess", "raluca", None, "2015-03-22", "19:15", "London", "Round reading room", 0, "")
    add_session(12, "Pool", "leif", None, "2015-03-23", "19:15", "Aberdeen", "QM", 0, "")
    add_session(13, "Pool", "jack", None, "2015-03-20", "19:15", "London", "O2 Arena", 1, "")
    add_session(14, "Chess", "john", None, "2015-03-19", "19:15", "Edinburgh", "Tesco Arena", 0, "")
    add_session(15, "Pool", "leif", None, "2015-03-20", "19:15", "London", "GUU", 1, "")

    # Offers.
    add_offer(1, "raluca")
    add_offer(1, "john")
    add_offer(1, "martynas")
    add_offer(1, "tomasz")
    add_offer(2, "jack")
    add_offer(3, "leif")
    add_offer(3, "leif")
    add_offer(4, "john")
    add_offer(4, "vlad")
    add_offer(4, "tomasz")
    add_offer(5, "leif")
    add_offer(6, "leif")
    add_offer(7, "leif")
    add_offer(7, "martynas")
    add_offer(8, "leif")
    add_offer(9, "raluca")
    add_offer(9, "helen")
    add_offer(9, "vlad")
    add_offer(10, "leif")
    add_offer(10, "raluca")
    add_offer(11, "helen")
    add_offer(13, "vlad")
    add_offer(13, "leif")
    add_offer(13, "raluca")
    add_offer(14, "helen")
    add_offer(15, "vlad")

    # Messages.
    add_message(1, "john", None, "2014-02-19", "18:21", "Hey mate, can you do 20:00?")
    add_message(1, "martynas", None, "2014-02-21", "19:13", "Do you have a racquet I could borrow?")
    add_message(1, "vlad", None, "2014-02-20", "12:21", "@john, naah, sorry, gotta be somewhere else by then...")
    add_message(1, "vlad", None, "2014-02-22", "16:33", "@martynas, you can borrow one from the desk, it's 1 pound.")

    add_message(2, "john", None, "2014-02-19", "18:21", "Hey mate, can we play a double? I could bring two of my friends(seriously hot)")
    add_message(2, "martynas", None, "2014-02-20", "19:13", "How long do you play man?")
    add_message(2, "tomasz", None, "2014-02-20", "12:21", "@john, ou yeee :D sure thing, bring them!")
    add_message(2, "tomasz", None, "2014-02-20", "21:33", "@martynas, around 2 years. Looking for someone skilled? I can ask a friend who's played for the past 10 years")

    add_message(3, "john", None, "2014-02-19", "18:21", "Hey, can you do 23:45?")
    add_message(3, "tomasz", None, "2014-02-21", "19:13", "Do you have a racquet I could borrow?")
    add_message(3, "helen", None, "2014-02-20", "12:21", "@john, naah, sorry, people tend to go to sleep at those times")
    add_message(3, "helen", None, "2014-02-21", "20:33", "@martynas, you can borrow one from the desk, it's 100 pounds")

    add_message(4, "john", None, "2014-02-19", "18:21", "Hey mate, do you have squash balls?")
    add_message(4, "martynas", None, "2014-02-21", "19:13", "Do you have a racquet I could borrow?")
    add_message(5, "vlad", None, "2014-02-20", "12:21", "I played with Kasparov. Can I join?")
    add_message(5, "leif", None, "2014-02-21", "16:33", "@vlad, I won with WATSON. You are no match for me")

# Start execution here!
if __name__ ==  '__main__':
    print "Starting PlayMaker population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playmaker_project.settings')
    from django.contrib.auth.models import User
    from playmaker.models import *
    populate()
