import re
from django import forms
from django.contrib.auth.models import User
from models import *
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)))
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=64, render_value=False)))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("The username already exists. Please try another one.")


class AddMessageToSessionForm(forms.Form):
    #id = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)), label=_("id"))
    session = forms.IntegerField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)), label="session")
    user_op = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)), label="user_op")
    user_viewer = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)), label="user_viewer")
    message = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=64)), label="message")

    def validate_user(self):
        if 'user_op' == 'user_viewer':
            raise forms.ValidationError("The host and bidder are the same.")
        return self.cleaned_data

    def validate_message(self):
        if 'message'.__eq__(self, None):
            raise forms.ValidationError("Empty message. Try again. ")
        return self.cleaned_data

    def validate_session(self):
        if 'session'.__eq__(self, None):
            raise forms.ValidationError("Empty session. Try again. ")
        return self.cleaned_data


class CreateSessionForm(forms.Form):
    sport = forms.Select()
    hostplayer = forms.IntegerField()
    date = forms.DateTimeField()
    time = forms.TimeField()
    city = forms.Select()
    location = forms.CharField()
    price = forms.FloatField()
    details = forms.CharField()





