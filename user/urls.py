from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='user-login'),
    path('logout', views.logout_user, name='user-logout'),

    path('signup', views.signup, name='user-signup'),
    path('change-profile', views.change_profile, name='user-change-profile'),
    path('seller-information', views.seller_information, name='user-seller-information'),
    path('seller-profile/<int:seller_id>/', views.seller_profile, name='seller-profile'),
    path('mypages', views.mypages, name='my-pages'),

    path('bookmark', views.handle_bookmark, name='create-bookmark'),
]