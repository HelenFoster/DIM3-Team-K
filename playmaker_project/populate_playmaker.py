import os

def add_city(city):
    print "City: " + city
    City.objects.get_or_create(city=city)

def add_sport(sport):
    print "Sport: " + sport
    Sport.objects.get_or_create(sport=sport)

def add_member(username, email, firstname, lastname):
    print "Member: " + username
    Member.objects.get_or_create(username=username,
        email=email,
        firstname=firstnmame,
        lasname=lastname
    )

def populate():
    add_city("Glasgow")
    add_city("Edinburgh")
    add_city("Stirling")
    add_sport("Squash")
    add_sport("Tennis")
    add_sport("Chess")

# Start execution here!
if __name__ == '__main__':
    print "Starting PlayMaker population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playmaker_project.settings')
    from playmaker.models import *
    populate()
