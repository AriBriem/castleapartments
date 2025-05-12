from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class Offers(models.Model):
    buyer = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    listing = models.ForeignKey('listing.Listings', on_delete=models.CASCADE)
    amount = models.IntegerField()
    post_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    status = models.TextField()
