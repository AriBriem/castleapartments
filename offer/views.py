from django.shortcuts import render

# Create your views here.

def make_offer(request, listing_id):
    return render(request, 'offer/offer-amount.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id})