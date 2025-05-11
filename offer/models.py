from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.

class Offers(models.Model):
    buyer_id = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    listing_id = models.ForeignKey('listing.Listings', on_delete=models.CASCADE)
    amount = models.IntegerField()
    post_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    status = models.TextField()
