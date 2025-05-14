from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# Create your models here.


class Postcodes(models.Model):
    postcode = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255)
    def __str__(self):
        return str(self.postcode)


class ListingType(models.Model):
    type = models.CharField(max_length=255)
    def __str__(self):
        return self.type


class Listings(models.Model):
    type = models.ForeignKey('listing.ListingType', on_delete=models.CASCADE)
    seller = models.ForeignKey('user.SellerProfile', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    sqr_meters = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    description = models.TextField()
    thumbnail_path = models.ImageField(upload_to="img/listingimages/")
    post_date = models.DateTimeField(default=timezone.now)
    sold = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.address


class ListingImage(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey('listing.Listings', on_delete=models.CASCADE, related_name='images')
    image_path = models.ImageField(max_length=255, upload_to="img/listingimages/", default='/static/img/default.jpg')
    def __str__(self):
        return self.image_path
    def image_url(self):
        return self.image_path.url