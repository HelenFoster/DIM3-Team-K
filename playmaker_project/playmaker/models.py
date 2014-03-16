__author__ = 'Vlad Schnakovszki'

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Foreign keys default their relationship to the primary key.

class City(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    city = models.CharField(unique=True, blank=False, null=False, max_length=64, )
    city_slug = models.SlugField(unique=True, blank=False, null=False, max_length=64, )

    # Stores the city slug.
    def save(self, *args, **kwargs):
        self.city_slug = slugify(self.city)
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'
    def __unicode__(self):
        return unicode(self.city)

class Message(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    user_op = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_op', )
    user_viewer = models.ForeignKey(User, unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_viewer', )
    date = models.DateField(blank=False, null=False, )
    time = models.TimeField(blank=False, null=False, )
    message = models.TextField(unique=False, blank=True, null=False, )

    def __unicode__(self):
        return unicode(self.id)

class Offer(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    session = models.ForeignKey('Session', unique=False, blank=False, null=False, on_delete=models.CASCADE, )
    guest = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, )

    class Meta:
        unique_together = (('session', 'guest'),)
    def __unicode__(self):
        return unicode(self.id)

class Session(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    sport = models.ForeignKey('Sport', unique=False, blank=False, null=False, to_field='sport', on_delete=models.CASCADE, )
    hostplayer = models.ForeignKey(User, unique=False, blank=False, null=False, on_delete=models.CASCADE, related_name='member_host', )
    guestplayer = models.ForeignKey(User, unique=False, blank=True, null=True, on_delete=models.CASCADE, related_name='member_guest', )
    date = models.DateField(blank=False, null=False, )
    time = models.TimeField(blank=False, null=False, )
    city = models.ForeignKey('City', unique=False, blank=False, null=False, to_field='city', on_delete=models.CASCADE, )
    location = models.CharField(max_length=64, unique=False, blank=False, null=False, )
    price = models.FloatField(unique=False, blank=False, null=False, default=0, )
    details = models.TextField(unique=False, blank=True, null=False, )

    def __unicode__(self):
        return unicode(self.id)

class Sport(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    sport = models.CharField(unique=True, blank=False, null=False, max_length=64, )
    sport_slug = models.SlugField(unique=True, blank=False, null=False, max_length=64, )

    # Stores the city slug.
    def save(self, *args, **kwargs):
        self.sport_slug = slugify(self.sport)
        super(Sport, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.sport)

class UserPreferredCities(models.Model):
    # id = AutoField(primary_key=True) added automatically.
    user = models.ForeignKey(User, unique=True, blank=False, null=False, on_delete=models.CASCADE, )
    city = models.ForeignKey('City', unique=False, blank=False, null=False, to_field='city', on_delete=models.CASCADE, )
