from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='user-login'),

    path('signup', views.signup, name='user-signup'),

    path('mypages', views.mypages, name='my-pages')
]