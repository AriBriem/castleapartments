from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from listing.models import Listings
from offer.models import Offers


# Create your views here.

def make_offer(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        expiry_date = request.POST.get('expiry_date')

        if not amount or not expiry_date:
            return render(request, 'offer/offer-amount.html', {
                'listing': listing,
                'error': 'All fields are required.',
            })

        Offers.objects.create(
            buyer_id=request.user,
            listing_id=listing,
            amount=amount,
            post_date=timezone.now(),
            expiry_date=expiry_date,
            status='Pending'
        )
        return redirect('listing-detail', listing_id=listing_id)
    return render(request, 'offer/offer-amount.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "listing": listing})

def finalize_offer(request, listing_id):
    return render(request, 'offer/offerfinalization.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id})