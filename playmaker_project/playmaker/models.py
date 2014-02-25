__author__ = 'Vlad Schnakovszki'

from django.db import models
from django.contrib.auth.models import User
# Added default values for some fields (e.g. unique=False) to be explicit.
# primary_key=True implies unique=True and null=False.
# Foreign keys default their relationship to the primary key.

class City(models.Model):
    city = models.CharField(primary_key=True, max_length=64, blank=False, db_column="city", )

    class Meta:
        verbose_name_plural = 'Cities'
    def __unicode__(self):
        return unicode(self.city)

class Message(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, db_column="session", )
    user_op = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_op', db_column="user_op", )
    user_viewer = models.ForeignKey(User, unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_viewer', db_column="user_viewer", )
    date = models.DateField(blank=False, null=False, db_column="date", )
    time = models.TimeField(blank=False, null=False, db_column="time", )
    message = models.TextField(unique=False, blank=True, null=False, db_column="message", )

    def __unicode__(self):
        return unicode(self.id)

class Offer(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, db_column="session", )
    guest = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, db_column="guest", )

    class Meta:
        unique_together = (('session', 'guest'),)
    def __unicode__(self):
        return unicode(self.id)

class Session(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    sport = models.ForeignKey('Sport', unique=False, blank=False, null=False, on_delete=models.CASCADE, db_column="sport", )
    hostplayer = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_host', db_column="hostplayer", )
    guestplayer = models.ForeignKey(User, unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_guest', db_column="guestplayer", )
    date = models.DateField(blank=False, null=False, db_column="date", )
    time = models.TimeField(blank=False, null=False, db_column="time", )
    city = models.ForeignKey('City', unique=False, blank=False, null=False, on_delete=models.CASCADE, db_column="city", )
    location = models.CharField(max_length=64, unique=False, blank=False, null=False, db_column="location", )
    price = models.FloatField(unique=False, blank=False, null=False, default=0, db_column="price", )
    details = models.TextField(unique=False, blank=True, null=False, db_column="details", )

    def __unicode__(self):
        return unicode(self.id)

class Sport(models.Model):
    sport = models.CharField(primary_key=True, max_length=64, blank=False, db_column="sport", )

    def __unicode__(self):
        return unicode(self.sport)