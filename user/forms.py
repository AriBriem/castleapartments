from django import forms
from user.models import *

class Login(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'password']