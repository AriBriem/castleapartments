from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from listing.models import Postcodes
from user.models import Country
from user.models import Users


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False, "error": "Invalid email or password."})
    return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False})

def signup(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        address = request.POST['address']
        personal_id = request.POST['personal_id']
        location = request.POST['location']
        postcode = request.POST['postcode']
        country = request.POST['country']
        if Users.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect("signup")
        user = Users.objects.create_user(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            address=address,
            personal_id=personal_id,
            location=location,
            postcode=postcode,
            country=country
        )
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect("login")
    return render(request, 'user/signup.html', {"show_navbar": False, "show_footer": False, "country": countries, "postcodes": postcodes})

def change_profile(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    return render(request, 'user/changeprofile.html', {"show_navbar": False, "show_footer": False, "country": countries, "postcodes": postcodes})

def seller_information(request):
    return render(request, 'user/sellerinformation.html', {"show_navbar": False, "show_footer": False})

def mypages(request):
    return render(request, 'user/mypages.html', {"show_navbar": True, "show_footer": True})