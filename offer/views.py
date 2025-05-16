from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from listing.models import Listings, Postcodes
from offer.models import Offers
from payment.models import Payments
from user.models import Country
from utils import get_postcodes_by_location

def make_offer(request, listing_id):
    #Check if user is authenticated in case they somehow get into the offer-amount page before logging in
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    listing = get_object_or_404(Listings, id=listing_id)
    #Make sure that the user does not send an offer to himself
    if listing.seller.user == user:
        return redirect('/listing/%d' % listing.id)
    #Check if the listing is sold in case that the make offer button appears even when a property is sold
    if listing.sold:
        return redirect('/listing/%d' % listing.id)
    if request.method == 'POST':
        raw_amount = request.POST.get('amount')
        #Convert amount to int without any dots
        amount = int(raw_amount.replace('.', ''))
        expiry_date = request.POST.get('expiry_date')

        #Check if everything is filled in
        if not amount or not expiry_date:
            return render(request, 'offer/offer-amount.html', {
                'listing': listing,
                'error': 'All fields are required.',
                'show_navbar': False,
                'show_footer': False,
            })

        #Create a new offer
        Offers.objects.create(
            buyer=request.user,
            listing=listing,
            amount=amount,
            post_date=timezone.now(),
            expiry_date=expiry_date,
            status='Pending'
        )
        messages.success(request, "Tilboð sent.")
        #Redirects to the listing itself
        return redirect('listing-detail', listing_id=listing_id)
    return render(request, 'offer/offer-amount.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "listing": listing})

def change_offer(request, listing_id, offer_id):
    # Check if user is authenticated in case they somehow get into the offer-change page before logging in
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    offer = Offers.objects.get(id=offer_id)
    listing = Listings.objects.get(id=listing_id)
    if request.method == 'POST':
        raw_amount = request.POST.get('amount')
        # Convert amount to int without any dots
        amount = int(raw_amount.replace('.', ''))
        expiry_date = request.POST.get('expiry_date')

        # Check if everything is filled in
        if not amount or not expiry_date:
            return render(request, 'offer/offer-change.html', {
                'listing': listing,
                'error': 'All fields are required.',
                'show_navbar': False,
                'show_footer': False,
            })

        #Change the offer
        offer.amount = amount
        offer.expiry_date = expiry_date
        offer.status = 'Pending'
        offer.save()
        messages.success(request, "Tilboð endursent.")
        # Redirects to the listing itself
        return redirect('listing-detail', listing_id=listing_id)
    return render(request, 'offer/offer-amount.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "listing": listing, "offer": offer})

def finalize_offer_contact(request, listing_id ,offer_id):
    # Check if user is authenticated in case they somehow get into the offerfinalization-contact page before logging in
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    # References a function in utils.py that is used in the html to filter the postcodes that appear in the select box by the location that the user selected
    postcodes_by_location = get_postcodes_by_location()
    countries = Country.objects.all()
    if request.method == 'POST':
        # Check if everything is filled in
        if request.POST.get('address') and request.POST.get('personal_id') and request.POST.get('location') and request.POST.get('postcode') and request.POST.get('country'):
            country_id = request.POST.get('country')
            country = Country.objects.get(id=country_id)
            postcode = request.POST.get('postcode')
            location = Postcodes.objects.get(postcode=postcode).location
            #Store data in request.session so that it persists between pages
            session_data = request.session.get('payment_data', {})
            session_data.update({
                'address': request.POST.get('address'),
                'personal_id': request.POST.get('personal_id'),
                'location': location,
                'postcode': postcode,
                'country': country_id,
                'country_name': country.name
            })
            request.session['payment_data'] = session_data
        else:
            #Failstate if everything isn't filled out
            data = request.session.get('payment_data')
            return render(request, 'offer/offerfinalization-payment.html', {
                "show_navbar": False,
                "show_footer": False,
                "listing_id": listing_id,
                "offer_id": offer_id,
                'data': data,
                'error': 'All fields are required.',
            })

        #Redirects to the next step (payment)
        return redirect('finalize-offer-payment', listing_id=listing_id, offer_id=offer_id)

    # We store data in request.session so that it appears on the page since the value in each of the input fields is of the form {{ data.<variable> }}
    session_data = request.session.get('payment_data', {})
    session_data.update({
        'address': user.address,
        'personal_id': user.personal_id,
        'location': user.postcode.location,
        'postcode': user.postcode.postcode,
        'country': user.country.id,
        'country_name': user.country.name
    })
    request.session['payment_data'] = session_data
    data = request.session.get('payment_data')
    context = {
        "show_navbar": False,
        "show_footer": False,
        "listing_id": listing_id,
        "offer_id": offer_id,
        "data": data,
        "postcodes_by_location": postcodes_by_location,
        "countries": countries
    }
    return render(request, 'offer/offerfinalization-contact.html', context)

def finalize_offer_payment(request, listing_id ,offer_id):
    # Check if user is authenticated in case they somehow get into the offerfinalization-payment page before logging in
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        #Get the payment method selected by the user
        selected_method = request.POST.get('payment-method')
        if selected_method == 'creditcard':
            # Check if everything is filled in
            if request.POST.get('card_carrier') and request.POST.get('card_number') and request.POST.get('expiry_date') and request.POST.get('cvc_number'):
                # Store data in request.session so that it persists between pages
                session_data = request.session.get('payment_data', {})
                session_data.update({
                    'payment_method': selected_method,
                    'card_carrier': request.POST.get('card_carrier'),
                    'card_number': request.POST.get('card_number'),
                    'expiry_date': request.POST.get('expiry_date'),
                    'cvc_number': request.POST.get('cvc_number'),
                })
                request.session['payment_data'] = session_data
            # Failstate if everything isn't filled out
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
            # Check if bank number is filled in
            if request.POST.get('bank_number'):
                # Store data in request.session so that it persists between pages
                session_data = request.session.get('payment_data', {})
                session_data.update({
                    'payment_method': selected_method,
                    'bank_number': request.POST.get('bank_number'),
                })
                request.session['payment_data'] = session_data
            # Failstate if everything isn't filled out
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
            # Check if the name of the lender is filled in
            if request.POST.get('lender'):
                # Store data in request.session so that it persists between pages
                session_data = request.session.get('payment_data', {})
                session_data.update({
                    'payment_method': selected_method,
                    'lender': request.POST.get('lender'),
                })
                request.session['payment_data'] = session_data
            # Failstate if everything isn't filled out
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

        #Redirect to final step (summary)
        return redirect('finalize-offer-summary', listing_id=listing_id, offer_id=offer_id)

    data = request.session.get('payment_data')
    return render(request, 'offer/offerfinalization-payment.html', {"show_navbar": False, "show_footer": False, "listing_id": listing_id, "offer_id": offer_id, "data": data})

def summary(request, listing_id, offer_id):
    # Check if user is authenticated in case they somehow get into the summary page before logging in
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    data = request.session.get('payment_data')
    if request.method == 'POST':
        #Changes user data just in case the user changed the contact information
        user = request.user
        user.address = data['address']
        user.personal_id = data['personal_id']
        user.postcode = Postcodes.objects.get(postcode=data['postcode'])
        user.country = Country.objects.get(id=data['country'])
        user.save()
        the_offer = Offers.objects.get(id=offer_id)
        #Creates a Payments instance
        Payments.objects.create(
            offer=the_offer,
            amount=the_offer.amount,
            time=the_offer.post_date,
            method=data['payment_method']
        )
        #Deletes payment_data
        del request.session['payment_data']
        messages.success(request, "Þú hefur klárað tilboðið þitt.")
        #Redirects to my pages
        return redirect('my-pages')

    context = {}

    return render(request, 'offer/summary.html',{"show_navbar": False, "show_footer": False, "listing_id":listing_id, "offer_id":offer_id, "data": data})