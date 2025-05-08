from django.shortcuts import render

from listing.models import Postcodes
from user.models import Country


# Create your views here.
def login(request):
    return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False})

def signup(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    return render(request, 'user/signup.html', {"show_navbar": False, "show_footer": False, "country": countries, "postcodes": postcodes})

def change_profile(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    return render(request, 'user/changeprofile.html', {"show_navbar": False, "show_footer": False, "country": countries, "postcodes": postcodes})

def seller_information(request):
    return render(request, 'user/sellerinformation.html', {"show_navbar": False, "show_footer": False})