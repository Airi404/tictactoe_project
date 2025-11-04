from django import forms
from .models import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['room_name']
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full px-3 py-2 rounded bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")