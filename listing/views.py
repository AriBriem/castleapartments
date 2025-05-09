from django.http import HttpResponse
from django.shortcuts import render
from listing.models import ListingType
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
    return render(request, 'listing/createlisting.html', {"show_navbar": False, "show_footer": True, "postcode": postcodes, "type": types})