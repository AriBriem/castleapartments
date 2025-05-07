from django.urls import path, include
from . import views

urlpatterns = [
    path('listings/<int:listing_id>/offers/create', views.make_offer, name='make-offer')
]