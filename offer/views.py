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

def change_offer(request, listing_id, offer_id):
    offer = Offers.objects.get(id=offer_id)
    listing = Listings.objects.get(id=listing_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        expiry_date = request.POST.get('expiry_date')

        if not amount or not expiry_date:
            return render(request, 'offer/offer-change.html', {
                'listing': listing,
                'error': 'All fields are required.',
                'show_navbar': False,
                'show_footer': False,
            })

        offer.amount = amount
        offer.expiry_date = expiry_date
        offer.status = 'Pending'
        offer.save()
        return redirect('listing-detail', listing_id=listing_id)
    return render(request, 'offer/offer-amount.html',
                  {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "listing": listing, "offer": offer})

def finalize_offer_contact(request, listing_id ,offer_id):
    if request.method == 'POST':
        if request.POST.get('address') and request.POST.get('personal_id') and request.POST.get('location') and request.POST.get('postcode') and request.POST.get('country'):
            request.session['payment_data'] = {
                'address': request.POST.get('address'),
                'personal_id': request.POST.get('personal_id'),
                'location': request.POST.get('location'),
                'postcode': request.POST.get('postcode'),
                'country': request.POST.get('country'),
            }
        else:
            data = request.session.get('payment_data')
            return render(request, 'offer/offerfinalization-payment.html', {
                "show_navbar": False,
                "show_footer": False,
                "listing_id": listing_id,
                "offer_id": offer_id,
                'data': data,
                'error': 'All fields are required.',
            })


        return redirect('finalize-offer-payment', listing_id=listing_id, offer_id=offer_id)

    data = request.session.get('payment_data')
    return render(request, 'offer/offerfinalization-contact.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "offer_id": offer_id, "data": data})

def finalize_offer_payment(request, listing_id ,offer_id):
    if request.method == 'POST':
        selected_method = request.POST.get('payment-method')
        if selected_method == 'creditcard':
            if request.POST.get('card_carrier') and request.POST.get('card_number') and request.POST.get('expiry_date') and request.POST.get('cvc_number'):
                request.session['payment_data'] = {
                    'payment_method': selected_method,
                    'card_carrier': request.POST.get('card_carrier'),
                    'card_number': request.POST.get('card_number'),
                    'expiry_date': request.POST.get('expiry_date'),
                    'cvc_number': request.POST.get('cvc_number'),
                }
            else:
                data = request.session.get('payment_data')
                return render(request, 'offer/offerfinalization-payment.html', {
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
                return render(request, 'offer/offerfinalization-payment.html', {
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
                return render(request, 'offer/offerfinalization-payment.html', {
                    "show_navbar": False,
                    "show_footer": False,
                    "listing_id": listing_id,
                    "offer_id": offer_id,
                    'data': data,
                    'error': 'All fields are required.',
                })


        return redirect('finalize-summary', listing_id=listing_id, offer_id=offer_id)

    data = request.session.get('payment_data')
    return render(request, 'offer/offerfinalization-payment.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "offer_id": offer_id, "data": data})

def summary(request, listing_id, offer_id):
    data = request.session.get('payment_data')
    if request.method == 'POST':
        user = request.user
        user.address = data['address']
        user.personal_id = data['personal_id']
        user.location = data['location']
        user.postcode = data['postcode']
        user.country = data['country']
        user.save()
        the_offer = Offers.objects.get(id=offer_id)
        Payments.objects.create(
            offer=the_offer,
            amount=the_offer.amount,
            time=the_offer.post_date,
            method=data['payment_method']
        )
        del request.session['payment_data']
        return redirect('my-pages')

    return render(request, 'offer/summary.html',{"show_navbar": False, "show_footer": False, "listing_id":listing_id, "offer_id":offer_id, "data": data})