from django.urls import path, include
from . import views

urlpatterns = [
    path('listings/<int:listing_id>/offers/create', views.make_offer, name='make-offer'),
    path('listings/<int:listing_id>/offers/<int:offer_id>/change', views.change_offer, name='change-offer'),
    path('listings/<int:listing_id>/offers/<int:offer_id>/finalize/contact', views.finalize_offer_contact, name='finalize-offer-contact'),
    path('listings/<int:listing_id>/offers/<int:offer_id>/finalize/payment', views.finalize_offer_payment, name='finalize-offer-payment'),
    path('listing/<int:listing_id>/offers/<int:offer_id>/finalize/summary', views.summary, name='finalize-offer-summary')
]