from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'listing/index.html', {"show_navbar": True, "show_footer": True})

def get_listing_by_id(request, listing_id):
    return render(request, 'listing/listing.html', {"listing_id": listing_id})