from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class EmergencyServiceForm(forms.ModelForm):
    class Meta:
        model = EmergencyService
        exclude = ['availability']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'rating']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date_time', 'description']

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'id': 'username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 'data-toggle': 'password',
                'id': 'password', "style": 'height:5vh;'
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'id': 'username',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 'data-toggle': 'password',
                'id': 'password',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 'data-toggle': 'password',
                'id': 'password'
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'id': 'email'
            }
        )
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",'id':'contact_number'
            }
        )  
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'is_admin', 'is_volunteer', 'is_public')

class VolunteerOpportunityForm(forms.ModelForm):
    class Meta:
        model = VolunteerOpportunity
        exclude = ['created_by', 'created_at']

class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['message']