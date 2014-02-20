__author__ = 'Vlad Schnakovszki'

from django.db import models

# Added default values for some fields (e.g. unique=False) to be explicit.
# primary_key=True implies unique=True and null=False.
# Foreign keys default their relationship to the primary key.

class City(models.Model):
    city = models.CharField(primary_key=True, max_length=64, blank=False, )

    class Meta:
        verbose_name_plural = 'Cities'
    def __unicode__(self):
        return unicode(self.city)

class Member(models.Model):
    username = models.CharField(primary_key=True, max_length=64, blank=False, )
    email = models.EmailField(max_length=64, unique=True, blank=False, null=False, )
    firstname = models.CharField(max_length=64, unique=False, blank=False, null=False, )
    lastname = models.CharField(max_length=64, unique=False, blank=False, null=False, )

    def __unicode__(self):
        return unicode(self.username)

class Message(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    user_op = models.ForeignKey('Member', unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_op', )
    user_viewer = models.ForeignKey('Member', unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_viewer', )
    date = models.DateField(blank=False, null=False, )
    time = models.TimeField(blank=False, null=False, )
    message = models.TextField(unique=False, blank=True, null=False, )

    def __unicode__(self):
        return unicode(self.id)

class Offer(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    guest = models.ForeignKey('Member', unique=False, blank=False, null=False, on_delete=models.CASCADE, )

    def __unicode__(self):
        return unicode(self.id)

class Session(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    sport = models.ForeignKey('Sport', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    hostplayer = models.ForeignKey('Member', unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_host', )
    guestplayer = models.ForeignKey('Member', unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_guest', )
    date = models.DateField(blank=False, null=False, )
    time = models.TimeField(blank=False, null=False, )
    city = models.ForeignKey('City', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    location = models.CharField(max_length=64, unique=False, blank=False, null=False, )
    price = models.FloatField(unique=False, blank=False, null=False, default=0, )
    details = models.TextField(unique=False, blank=True, null=False, )

    def __unicode__(self):
        return unicode(self.id)

class Sport(models.Model):
    sport = models.CharField(primary_key=True, max_length=64, blank=False, )

    def __unicode__(self):
        return unicode(self.sport)