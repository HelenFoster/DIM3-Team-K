__author__ = 'Vlad Schnakovszki'

from django.contrib import admin
from models import *

class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(City)

class MemberAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'firstname', 'lastname', ]

admin.site.register(Member)

class MessageAdmin(admin.ModelAdmin):
    search_fields = ['session', 'user_op', 'user_viewer', ]
    list_filter = ['date', ]

admin.site.register(Message)

class OfferAdmin(admin.ModelAdmin):
    search_fields = ['session', 'guest', ]

admin.site.register(Offer)

class SessionAdmin(admin.ModelAdmin):
    search_fields = ['sport', 'hostplayer', 'guestplayer', 'city', 'location', ]
    list_filter = ['sport', 'city', 'date', ]

admin.site.register(Session)

class SportAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sport)
