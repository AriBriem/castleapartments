from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='listing-index'),
    path('listing/<int:listing_id>/', views.get_listing_by_id, name='listing-detail'),
    path('listing/', views.create_listing, name='listing-create')
]