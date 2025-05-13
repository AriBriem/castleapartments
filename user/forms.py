from django import forms
from user.models import *

class Login(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'password']



class SignUp(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'email', 'phone_number', 'password', 'address', 'personal_id', '']