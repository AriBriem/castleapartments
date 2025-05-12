from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from listing.models import ListingType
from listing.models import Postcodes, Listings, ListingType
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

    types = ListingType.objects.all()

    context = {
        'show_navbar': True,
        'show_footer': True,
        'postcodes_by_location': postcodes_by_location,
        'types': types,
    }


    return render(request, 'listing/index.html', context)

def get_listing_by_id(request, listing_id):
    return render(request, 'listing/listing.html', {"show_navbar": True, "show_footer": False, "listing_id": listing_id})

def filter_listings(request):
    postcode_ids = request.GET.get('postcodes')
    type_ids = request.GET.get('types')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    meters_from = request.GET.get('meters_from')
    meters_to = request.GET.get('meters_to')

    filters = Q()

    if postcode_ids:
        postcode_ids = postcode_ids.split(',')
        filters &= Q(postcode_id__in=postcode_ids)
    if type_ids:
        type_ids = type_ids.split(',')
        filters &= Q(type_id__in=type_ids)
    #if price_from:
    #    filters &= Q(price__gte=price_from)
    #if price_to:
    #    filters &= Q(price__lte=price_to)
    if meters_from:
        filters &= Q(sqr_meters__gte=meters_from)
    if meters_to:
        filters &= Q(sqr_meters__lte=meters_to)

    if filters:
        listings = Listings.objects.filter(filters)
    else:
        listings = Listings.objects.all()


    return render(request, 'partials/property_list.html', {"listings": listings})

def create_listing(request):
    postcodes = Postcodes.objects.all()
    types = ListingType.objects.all()
    if request.method == 'POST':
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        type = request.POST.get('type')
        sqr_meters = request.POST.get('sqr_meters')
        rooms = request.POST.get('rooms')
        bathrooms = request.POST.get('bathrooms')
        bedrooms = request.POST.get('bedrooms')
        description = request.POST.get('description')
        thumbnail_path = request.FILES.get('listing_image')

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