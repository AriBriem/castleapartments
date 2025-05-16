from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from listing.models import Postcodes, Listings
from offer.models import Offers
from payment.models import Payments
from user.models import Country, SellerProfile
from user.models import Country, SellerProfile, Bookmarks
from user.models import Users
from django.http import HttpResponse
import json

from utils import get_postcodes_by_location

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Aðgangur skráður inn")
            return redirect('listing-index')
        else:
            return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False, "error": "Invalid email or password."})
    return render(request, 'user/login.html', {"show_navbar": False, "show_footer": False})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('listing-index')

def signup(request):
    postcodes_by_location = get_postcodes_by_location()
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
            postcode = Postcodes.objects.get(postcode=postcode)
        else:
            postcode = None
        if country:
            country = Country.objects.get(id=country)
        else:
            country = None

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
                postcode=postcode,
                country=country,
                profile_image_path=profile_image_path,
                cover_image_path=cover_image_path
            )
            messages.success(request, "Aðgangur skapaður. Þú getur núna skráð þig inn")
            return redirect("user-login")
        except ValueError as e:
            print(f"Signup error: {e}")
            messages.error(request, str(e))
            return redirect("user-signup")

    context = {
        "show_navbar": False,
        "show_footer": False,
        "countries": countries,
        "error": messages.error,
        'postcodes_by_location': postcodes_by_location,
    }
    return render(request, 'user/signup.html', context)

def change_profile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    postcodes_by_location = get_postcodes_by_location()
    countries = Country.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        personal_id = request.POST.get('personal_id')
        location = request.POST.get('location')
        postcode = get_object_or_404(Postcodes, postcode=request.POST.get('postcode'))
        country = get_object_or_404(Country, id=request.POST.get('country'))
        profile_image_path = request.FILES.get('profile_image')
        cover_image_path = request.FILES.get('cover_image')
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
        if postcode:
            user.postcode = postcode
        if country:
            user.country = country
        if profile_image_path:
            user.profile_image_path = profile_image_path
        if cover_image_path:
            user.cover_image_path = cover_image_path
        print(new_password)
        if new_password:
            if not user.check_password(new_password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Prófíll breyttur.")
        return redirect('my-pages')

    context = {
        "show_navbar": False,
        "show_footer": False,
        "countries": countries,
        "postcodes_by_location": postcodes_by_location,
        "user": user
    }
    return render(request, 'user/changeprofile.html', context)

def seller_information(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    from_listing = request.GET.get('from') == 'listing'
    if request.method == 'POST':
        bio = request.POST.get('bio')
        logo_path = request.FILES.get('logo_path')
        is_company = request.POST.get('is_company')

        if not bio or is_company not in ['yes', 'no']:
            return render(request, 'user/sellerinformation.html', {
                'show_navbar': False,
                'show_footer': False,
                'error': 'Settu inn lýsingu og veldu einstakling eða fyrirtæki',
            })

        if is_company == "yes":
            is_company = True
        elif is_company == "no":
            is_company = False

        SellerProfile.objects.create(
            user_id=request.user.id,
            logo_path=logo_path,
            bio=bio,
            is_company=is_company
        )
        if from_listing:
            messages.success(request, "Seller information created successfully.")
            return redirect('listing-create')
        messages.success(request, "Seller information changed successfully.")
        return redirect('listing-index')
    return render(request, 'user/sellerinformation.html', {"show_navbar": False, "show_footer": False, "from_listing": from_listing})

def change_seller_information(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    try:
        seller_information = SellerProfile.objects.get(user=request.user)
    except:
        return redirect('user-seller-information')

    if request.method == 'POST':
        bio = request.POST.get('bio')
        logo_path = request.FILES.get('logo_path')
        is_company = request.POST.get('is_company')

        if not bio or is_company not in ['yes', 'no']:
            return render(request, 'user/sellerinformation.html', {
                'show_navbar': False,
                'show_footer': False,
                'error': 'Settu inn lýsingu og veldu einstakling eða fyrirtæki',
            })
        if is_company == "yes":
            is_company = True
        elif is_company == "no":
            is_company = False

        seller_information.bio = bio
        seller_information.logo_path = logo_path
        seller_information.is_company = is_company
        seller_information.save()
        messages.success(request, "Seljanda prófíl breyttur.")
        return redirect('my-pages')
    return render(request, 'user/changesellerinformation.html',{"show_navbar": False, "show_footer": False})

def seller_profile(request, seller_id):
    seller = get_object_or_404(SellerProfile, id=seller_id)
    return render(request, 'user/sellerprofile.html', {"show_navbar": True, "show_footer": True, "seller": seller})


def mypages(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    seller_profile = SellerProfile.objects.filter(user=request.user).first()

    if seller_profile:
        incoming_offers = Offers.objects.filter(listing__seller__user=user)
        listings = Listings.objects.filter(seller__user=user)
        if request.method == 'POST':
            offer_id = request.POST.get('offer_id')
            listing_id = request.POST.get('listing_id')
            accepted = request.POST.get('accepted')
            contingent = request.POST.get('contingent')
            rejected = request.POST.get('rejected')
            offer = Offers.objects.get(id=offer_id)
            listing = Listings.objects.get(id=listing_id)
            islenska = ""
            if accepted:
                offer.status = 'Accepted'
                listing.sold = True
                islenska = "Samþykkt"
            elif contingent:
                offer.status = 'Contingent'
                listing.sold = True
                islenska = "Skilyrt"
            elif rejected:
                offer.status = 'Rejected'
                islenska = "Hafnað"

            offer.save()
            listing.save()
            messages.success(request, f"Tilboð merkt sem {islenska}")
    else:
        incoming_offers = None
        listings = None

    outgoing_offers = Offers.objects.filter(buyer=request.user)
    for offer in outgoing_offers:
        offer.has_payment = Payments.objects.filter(offer=offer).exists()
        
    context = {
        'show_navbar': True,
        'show_footer': True,
        'incoming_offers': incoming_offers,
        'outgoing_offers': outgoing_offers,
        'listings': listings,
        'user': user,
        'seller_profile': seller_profile,
    }
    return render(request, 'user/mypages.html', context)

def handle_bookmark(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user-login')

    try:
        data = json.loads(request.body)
        listing_id = data.get('listingId')
        listing = Listings.objects.get(id=listing_id)
    except:
        return HttpResponse(status=400)

    if request.method == 'POST':
        Bookmarks.objects.create(user=user, listing=listing)
        return HttpResponse(status=201)
    elif request.method == 'DELETE':
        Bookmarks.objects.filter(user=user, listing=listing).delete()
        return HttpResponse(status=204)

    return HttpResponse(status=405)
