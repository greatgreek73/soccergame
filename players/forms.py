from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateClubForm(forms.Form):
    name = forms.CharField(label='Club Name', max_length=100)
    country = forms.ChoiceField(label='Country', choices=[('Russia', 'Russia'), ('USA', 'USA'), ('Greece', 'Greece'), ('Italy', 'Italy')])

class GeneratePlayerForm(forms.Form):
    position = forms.ChoiceField(label='Position', choices=Player.POSITIONS)