from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, DateInput, PasswordInput, TimeInput, SplitDateTimeWidget, URLInput
from django import forms

from makethedifference.models import Event, User, Comment


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio', 'website']


class UserDeleteForm(ModelForm):
    class Meta:
        model = User
        fields = []


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'cause', 'location', 'start_date', 'end_date', 'image', 'tag']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'location': URLInput(attrs={'placeholder': 'Enter Google Maps URL here'})
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']
        #
        # widgets = {
        #     "password1": PasswordInput(
        #         attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password1'}),
        # }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
