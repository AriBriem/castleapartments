from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from listing.models import Listings
from offer.forms import PaymentForm
from offer.models import Offers
from payment.models import Payments


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
                'show_navbar': False,
                'show_footer': False,
            })

        Offers.objects.create(
            buyer=request.user,
            listing=listing,
            amount=amount,
            post_date=timezone.now(),
            expiry_date=expiry_date,
            status='Pending'
        )
        return redirect('listing-detail', listing_id=listing_id)
    return render(request, 'offer/offer-amount.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "listing": listing})

def finalize_offer(request, listing_id ,offer_id):
    if request.method == 'POST':
        selected_method = request.POST.get('payment-method')
        if selected_method == 'creditcard':
            if request.POST.get('card-carrier') and request.POST.get('card-number') and request.POST.get('expiry-date') and request.POST.get('cvc_number'):
                request.session['payment_data'] = {
                    'payment_method': selected_method,
                    'card_carrier:': request.POST.get('card_carrier'),
                    'card_number': request.POST.get('card_number'),
                    'expiry_date': request.POST.get('expiry_date'),
                    'cvc_number': request.POST.get('cvc_number'),
                }
            else:
                data = request.session.get('payment_data')
                return render(request, 'offer/offerfinalization.html', {
                    "show_navbar": False,
                    "show_footer": False,
                    "listing_id": listing_id,
                    "offer_id": offer_id,
                    'data': data,
                    'error': 'All fields are required.',
                })

        elif selected_method == 'transfer':
            if request.POST.get('bank_number'):
                request.session['payment_data'] = {
                    'payment_method': selected_method,
                    'bank_number': request.POST.get('bank_number'),
                }
            else:
                data = request.session.get('payment_data')
                return render(request, 'offer/offerfinalization.html', {
                    "show_navbar": False,
                    "show_footer": False,
                    "listing_id": listing_id,
                    "offer_id": offer_id,
                    'data': data,
                    'error': 'All fields are required.',
                })

        elif selected_method == 'loan':
            if request.POST.get('lender'):
                request.session['payment_data'] = {
                    'payment_method': selected_method,
                    'lender': request.POST.get('lender'),
                }
            else:
                data = request.session.get('payment_data')
                return render(request, 'offer/offerfinalization.html', {
                    "show_navbar": False,
                    "show_footer": False,
                    "listing_id": listing_id,
                    "offer_id": offer_id,
                    'data': data,
                    'error': 'All fields are required.',
                })


        return redirect('finalize-offer-summary', listing_id=listing_id, offer_id=offer_id)

    data = request.session.get('payment_data')
    return render(request, 'offer/offerfinalization.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "offer_id": offer_id, "data": data })

def summary(request, listing_id, offer_id):
    data = request.session.get('payment_data')
    if request.method == 'POST':
        the_offer = Offers.objects.filter(id=data.offer_id)
        Payments.objects.create(
            offer=data.offer_id,
            amount=the_offer.amount,
            time=the_offer.post_date,
            method=data.payment_method
        )

        return redirect('my-pages')

    return render(request, 'offer/offerfinalization.html',{"show_navbar": False, "show_footer": False, "listing_id":listing_id, "offer_id":offer_id, "data": data})