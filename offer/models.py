from django.contrib.auth.models import User
from django.db import models

from listing.models import Listings
from user.models import Users

# Create your models here.

class Offers(models.Model):
    offerID = models.IntegerField(primary_key=True)
    buyerID = models.ForeignKey(Users, on_delete=models.CASCADE)
    listingID = models.ForeignKey(Listings, on_delete=models.CASCADE)
    amount = models.IntegerField()
    postDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    status = models.TextField()
