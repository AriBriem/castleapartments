from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from listing.models import ListingType, ListingImage, Postcodes, Listings
from offer.models import Offers
from user.models import SellerProfile, Bookmarks

from utils import get_postcodes_by_location

def index(request):
    postcodes_by_location = get_postcodes_by_location()

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
    user = request.user
    listing = get_object_or_404(Listings, id=listing_id)
    listing_images = ListingImage.objects.filter(listing=listing)
    image_urls = [img.image_path.url for img in listing_images]
    bookmarked = False

    if user.is_authenticated:
        bookmarked = Bookmarks.objects.filter(user=request.user, listing=listing).exists()

    try:
        offer = Offers.objects.get(buyer=user.id, listing=listing)
    except ObjectDoesNotExist:
        offer = None

    context = {
        "show_navbar": True,
        "show_footer": False,
        "listing": listing,
        "images": image_urls,
        "offer": offer,
        "bookmarked": bookmarked,
    }

    return render(request, 'listing/listing.html', context)

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
    show_bookmark = request.GET.get('show_bookmark') == 'true'

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

    if is_bookmark:
        if request.user.is_authenticated:
            listings = listings.filter(bookmarks__user=request.user)
        else:
            listings = Listings.objects.none()

    return render(request, 'partials/property_list.html', {"listings": listings, "bookmarks": bookmarks, "show_bookmark": show_bookmark})

def create_listing(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user-login')

    try:
        seller = SellerProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect('/seller-information?from=listing')

    postcodes_by_location = get_postcodes_by_location()
    types = ListingType.objects.all()

    if request.method == 'POST':
        #Check if everything is filled out
        if request.POST.get('address') and request.POST.get('postcode') and request.POST.get('type') and request.POST.get('sqr_meters') and request.POST.get('rooms') and request.POST.get('bathrooms') and request.POST.get('bedrooms') and request.POST.get('description') and request.FILES.get('thumbnail') and request.POST.get('price').replace(".", ""):
            #Get all input from user
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

            #Create the listing
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
            #Store the images in ListingImage
            for file in listing_images:
                ListingImage.objects.create(listing=listing, image_path=file)
            #Make sure that the listing was properly created
            listing = Listings.objects.filter(seller=seller, address=address).first()
            if listing:
                messages.success(request, "Eign skráð.")
                return redirect("listing-detail", listing_id=listing.id)
        else:
            context = {
                "show_navbar": False,
                "show_footer": False,
                "error": 'All fields are required.',
                "postcodes_by_location": postcodes_by_location,
                "types": types
            }
            return render(request, 'listing/createlisting.html', context)


    context = {
        "show_navbar": False,
        "show_footer": False,
        "postcodes_by_location": postcodes_by_location,
        "types": types
    }
    return render(request, 'listing/createlisting.html', context)