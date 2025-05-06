from django.db import models

# Create your models here.
from user.models import SellerProfile

class Postcodes(models.Model):
    postcode = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=255)
    def __str__(self):
        return self.postcode


class ListingType(models.Model):
    typeID = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255)
    def __str__(self):
        return self.type



class Listings(models.Model):
    listingID = models.IntegerField(primary_key=True)
    typeID = models.ForeignKey(ListingType, on_delete=models.CASCADE)
    sellerID = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    sqrMeters = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    postcode = models.ForeignKey(Postcodes, on_delete=models.CASCADE)
    description = models.TextField()
    thumbnailPath = models.CharField(max_length=255)
    postDate = models.DateTimeField()

    def __str__(self):
        return self.listingID


class ListingImage(models.Model):
    listingID = models.ForeignKey(Listings, primary_key=True, on_delete=models.CASCADE)
    imagePath = models.CharField(max_length=255)
    def __str__(self):
        return self.imagePath