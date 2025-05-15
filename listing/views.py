from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from listing.models import ListingType, ListingImage
from listing.models import Postcodes, Listings, ListingType
from django.shortcuts import render, redirect, get_object_or_404
from listing.models import ListingType, Listings
from listing.models import Postcodes
from collections import defaultdict
from user.models import SellerProfile, Bookmarks

from offer.models import Offers
from user.models import SellerProfile, Users


def index(request):
    postcodes_by_location = defaultdict(list)
    for row in Postcodes.objects.values('postcode', 'location'):
        postcodes_by_location[row['location']].append(row['postcode'])
    postcodes_by_location = dict(postcodes_by_location)

    types = ListingType.objects.all()
    listing_count = Listings.objects.all().count()

    context = {
        'show_navbar': True,
        'show_footer': True,
        'postcodes_by_location': postcodes_by_location,
        'types': types,
        'listing_count': listing_count,
    }


    return render(request, 'listing/index.html', context)

def get_listing_by_id(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    listing_images = ListingImage.objects.filter(listing=listing)
    image_urls = [img.image_path.url for img in listing_images]
    buyer = Users.objects.get(id=request.user.id)
    try:
        offer = Offers.objects.get(buyer=buyer, listing=listing)
    except ObjectDoesNotExist:
        offer = None

    return render(request, 'listing/listing.html', {"show_navbar": True, "show_footer": False, "listing": listing, "images": image_urls, "offer": offer})

def filter_listings(request):
    postcode_ids = request.GET.get('postcodes')
    type_ids = request.GET.get('types')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    meters_from = request.GET.get('meters_from')
    meters_to = request.GET.get('meters_to')
    seller = request.GET.get('seller_id')
    search = request.GET.get('search')
    order_by = request.GET.get('order_by')
    is_bookmark = request.GET.get('bookmark') == 'true'

    filters = Q()

    if postcode_ids:
        postcode_ids = postcode_ids.split(',')
        filters &= Q(postcode_id__in=postcode_ids)
    if type_ids:
        type_ids = type_ids.split(',')
        filters &= Q(type_id__in=type_ids)
    if price_from:
        filters &= Q(price__gte=int(price_from)*1000000)
    if price_to:
        filters &= Q(price__lte=int(price_to)*1000000)
    if meters_from:
        filters &= Q(sqr_meters__gte=meters_from)
    if meters_to:
        filters &= Q(sqr_meters__lte=meters_to)
    if seller:
        filters &= Q(seller=seller)
    if search:
        filters &= Q(address__icontains=search)


    if filters:
        listings = Listings.objects.filter(filters)
    else:
        listings = Listings.objects.all()

    if order_by and order_by != 'undefined':
        listings = listings.order_by(order_by)

    if request.user.is_authenticated:
        bookmarks = Bookmarks.objects.filter(user=request.user).values_list('listing_id', flat=True)
    else:
        bookmarks = []

    print(is_bookmark)

    if is_bookmark:
        if request.user.is_authenticated:
            listings = listings.filter(bookmarks__user=request.user)
        else:
            listings = Listings.objects.none()

    return render(request, 'partials/property_list.html', {"listings": listings, "bookmarks": bookmarks})

def create_listing(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user-login')

    seller = SellerProfile.objects.get(user=request.user)
    if not seller:
        return redirect('/seller-information?from=listing')

    postcodes_by_location = defaultdict(list)
    for row in Postcodes.objects.values('postcode', 'location'):
        postcodes_by_location[row['location']].append(row['postcode'])
    postcodes_by_location = dict(postcodes_by_location)
    types = ListingType.objects.all()
    if request.method == 'POST':
        address = request.POST.get('address')
        postcode = Postcodes.objects.get(postcode = request.POST.get('postcode'))
        type = ListingType.objects.get(id=request.POST.get('type'))
        sqr_meters = request.POST.get('sqr_meters')[:-2]
        rooms = request.POST.get('rooms')
        bathrooms = request.POST.get('bathrooms')
        bedrooms = request.POST.get('bedrooms')
        description = request.POST.get('description')
        thumbnail_path = request.FILES.get('thumbnail')
        price = request.POST.get('price').replace(".", "")

        listing_images = request.FILES.getlist('listing_images')
        print(listing_images)

        if Listings.objects.filter(address=address).exists():
            messages.error(request, "Listing with this address already exists.")
            return redirect("listing-create")

        listing = Listings.objects.create(
            seller=seller,
            address=address,
            postcode=postcode,
            sqr_meters=sqr_meters,
            type=type,
            rooms=rooms,
            bathrooms=bathrooms,
            bedrooms=bedrooms,
            description=description,
            price = price,
            thumbnail_path=thumbnail_path
        )
        for file in listing_images:
            ListingImage.objects.create(listing=listing, image_path=file)
        messages.success(request, "Listing created successfully. You can now log in.")
        print("")
        listing = Listings.objects.filter(seller=seller, address=address).first()
        if listing:
            return redirect("listing-detail", listing_id=listing.id)
        return redirect("user-seller-information")

    context = {
        "show_navbar": False,
        "show_footer": False,
        "postcodes_by_location": postcodes_by_location,
        "types": types}
    return render(request, 'listing/createlisting.html', context)