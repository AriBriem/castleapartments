from django.db import models

# Create your models here.


class Postcodes(models.Model):
    postcode = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=255)
    def __str__(self):
        return self.postcode


class ListingType(models.Model):
    type = models.CharField(max_length=255)
    def __str__(self):
        return self.type


class Listings(models.Model):
    type_id = models.ForeignKey('listing.ListingType', on_delete=models.CASCADE)
    seller_id = models.ForeignKey('user.SellerProfile', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    sqr_meters = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    description = models.TextField()
    thumbnail_path = models.CharField(max_length=255)
    post_date = models.DateTimeField()

    def __str__(self):
        return self.listingID


class ListingImage(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey('listing.Listings', on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=255)
    def __str__(self):
        return self.imagePath