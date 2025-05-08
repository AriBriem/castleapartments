from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class Offers(models.Model):
    buyerID = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    listingID = models.ForeignKey('listing.Listings', on_delete=models.CASCADE)
    amount = models.IntegerField()
    postDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    status = models.TextField()
