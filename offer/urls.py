from django.urls import path, include
from . import views

urlpatterns = [
    path('listings/<int:listing_id>/offers/create', views.make_offer, name='make-offer'),
    path('listings/<int:listing_id>/offers/<int:offer_id>/finalize', views.finalize_offer, name='finalize-offer')
]