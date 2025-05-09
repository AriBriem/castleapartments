from django.shortcuts import render

from user.models import Country


# Create your views here.
def login(request):
    return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False})

def signup(request):
    return render(request, 'user/signup.html', {"show_navbar": False, "show_footer": False, "country": Country})

def mypages(request):
    return render(request, 'user/mypages.html', {"show_navbar": True, "show_footer": True})