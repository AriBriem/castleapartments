from django.http import HttpResponse
from django.shortcuts import render
from listing.models import ListingType
from listing.models import Postcodes
# Create your views here.
def index(request):
    return render(request, 'listing/index.html', {"show_navbar": True, "show_footer": True})

def get_listing_by_id(request, listing_id):
    return render(request, 'listing/listing.html', {"show_navbar": True, "show_footer": False, "listing_id": listing_id})

def create_listing(request):
    postcodes = Postcodes.objects.all()
    types = ListingType.objects.all()
    return render(request, 'listing/createlisting.html', {"show_navbar": False, "show_footer": False, "postcodes": postcodes, "types": types})