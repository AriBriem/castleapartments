from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='user-login'),

    path('signup', views.signup, name='user-signup'),
    path('change-profile', views.change_profile, name='user-change-profile'),
    path('seller-information', views.seller_information, name='user-seller-information'),
    path('signup', views.signup, name='user-signup'),

    path('mypages', views.mypages, name='my-pages')
]