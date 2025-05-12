from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from listing.models import Postcodes, Listings
from offer.models import Offers
from user.models import Country, SellerProfile
from user.models import Users


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('listing-index')
        else:
            return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False, "error": "Invalid email or password."})
    return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False})

def signup(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        address = request.POST.get('address')
        personal_id = request.POST.get('personal_id')
        location = request.POST.get('location')
        postcode = request.POST.get('postcode')
        country = request.POST.get('country')
        profile_image_path = request.FILES.get('profile_image')
        cover_image_path = request.FILES.get('cover_image')

        if postcode:
            postcode = Postcodes.objects.get(id=postcode)

        country = Country.objects.get(id=country) if country else None

        if Users.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect("user-signup")
        try:
            user = Users.objects.create_user(
                email=email,
                password=password,
                name=name,
                phone_number=phone_number,
                address=address,
                personal_id=personal_id,
                location=location,
                postcode=postcode,
                country=country,
                profile_image_path=profile_image_path,
                cover_image_path=cover_image_path
            )
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("user-login")
        except ValueError as e:
            print(f"Signup error: {e}")
            messages.error(request, str(e))
            return redirect("user-signup")
    return render(request, 'user/signup.html', {"show_navbar": False, "show_footer": False, "countries": countries, "postcodes": postcodes, "error": messages.error})

def change_profile(request):
    postcodes = Postcodes.objects.all()
    countries = Country.objects.all()
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        personal_id = request.POST.get('personal_id')
        location = request.POST.get('location')
        postcode = request.POST.get('postcode')
        country = request.POST.get('country')
        profile_image_path = request.FILES.get['profile_image']
        cover_image_path = request.FILES.get['cover_image']
        new_password = request.POST.get('new_password')


        if name:
            user.name = name
        if email and email != user.email:
            if Users.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "Email already in use.")
                return redirect('update_profile')
            user.email = email
        if phone:
            user.phone_number = phone
        if address:
            user.address = address
        if personal_id:
            user.personal_id = personal_id
        if location:
            user.location = location
        if postcode:
            user.postcode = postcode
        if country:
            user.country = country
        if profile_image_path:
            user.profile_image_path = profile_image_path
        if cover_image_path:
            user.cover_image_path = cover_image_path

        if new_password:
            if not user.check_password(new_password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('my-pages')
    return render(request, 'user/changeprofile.html', {"show_navbar": False, "show_footer": False, "country": countries, "postcodes": postcodes, "user": user})

def seller_information(request):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        logo_path = request.FILES.get('logo_path')
        is_company = request.POST.get('seller-type')
        if is_company == "yes":
            is_company = True
        elif is_company == "no":
            is_company = False


        if not bio or not is_company:
            return render(request, 'user/sellerinformation.html', {
                'show_navbar': False,
                'show_footer': False,
                'error': 'Settu inn lýsingu og veldu einstakling eða fyrirtæki',
            })

        SellerProfile.objects.create(
            user_id=request.user,
            logo_path=logo_path,
            bio=bio,
            is_company=is_company
        )
        return redirect('listing-index')
    return render(request, 'user/sellerinformation.html', {"show_navbar": False, "show_footer": False})

def mypages(request):
    offers = Offers.objects.all()
    listings = Listings.objects.all()
    users = Users.objects.all()
    return render(request, 'user/mypages.html', {"show_navbar": True, "show_footer": True, "offers": offers, "listings": listings, "users": users})