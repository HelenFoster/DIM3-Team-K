__author__ = 'Vlad Schnakovszki'

from django.contrib import admin
from models import *

class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(City, CityAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'user_op', 'user_viewer', 'date', 'time', 'message', ]
    search_fields = ['session', 'user_op', 'user_viewer', ]
    list_filter = ['date', ]

admin.site.register(Message, MessageAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ['session', 'guest', ]
    search_fields = ['session', 'guest', ]

admin.site.register(Offer, OfferAdmin)

class SessionAdmin(admin.ModelAdmin):
    list_display = ['sport', 'hostplayer', 'guestplayer', 'city', 'location', 'date', 'time', 'price', 'details', ]
    search_fields = ['sport', 'hostplayer', 'guestplayer', 'city', 'location', ]
    list_filter = ['sport', 'city', 'date', ]

admin.site.register(Session, SessionAdmin)

class SportAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sport, SportAdmin)
