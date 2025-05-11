from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from listing.models import ListingType, Listings
from listing.models import Postcodes
# Create your views here.
from collections import defaultdict


def index(request):
    postcodes_by_location = defaultdict(list)
    for row in Postcodes.objects.values('postcode', 'location'):
        postcodes_by_location[row['location']].append(row['postcode'])
    postcodes_by_location = dict(postcodes_by_location)
    return render(request, 'listing/index.html', {"show_navbar": True, "show_footer": True, 'postcodes_by_location': postcodes_by_location})

def get_listing_by_id(request, listing_id):
    return render(request, 'listing/listing.html', {"show_navbar": True, "show_footer": False, "listing_id": listing_id})

def filter_listings(request):
    return

def create_listing(request):
    postcodes = Postcodes.objects.all()
    types = ListingType.objects.all()
    if request.method == 'POST':
        address = request.POST['address']
        postcode = request.POST['postcode']
        type = request.POST['type']
        sqr_meters = request.POST['sqr_meters']
        rooms = request.POST['rooms']
        bathrooms = request.POST['bathrooms']
        bedrooms = request.POST['bedrooms']
        description = request.POST['description']
        thumbnail_path = request.FILES.get['listing_image']

        if Listings.objects.filter(address=address).exists():
            messages.error(request, "Listing with this address already exists.")
            return redirect("listing-create")
        listing = Listings.objects.create(
            seller_id=request.user.id,
            address=address,
            postcode=postcode,
            sqr_meters=sqr_meters,
            type=type,
            rooms=rooms,
            bathrooms=bathrooms,
            bedrooms=bedrooms,
            description=description,
            thumbnail_path=thumbnail_path
        )
        messages.success(request, "Listing created successfully. You can now log in.")
        if Listings.objects.filter(seller_id=request.user.id).exclude(address=address).exists():
            return redirect("listing-detail", listing_id=listing.id)
        return redirect("user-seller-information")
    return render(request, 'listing/createlisting.html', {"show_navbar": False, "show_footer": False, "postcodes": postcodes, "types": types})