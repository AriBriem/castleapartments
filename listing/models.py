from django.db import models

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
    typeID = models.ForeignKey('listing.ListingType', on_delete=models.CASCADE)
    sellerID = models.ForeignKey('user.SellerProfile', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    sqrMeters = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    description = models.TextField()
    thumbnailPath = models.CharField(max_length=255)
    postDate = models.DateTimeField()

    def __str__(self):
        return self.address


class ListingImage(models.Model):
    id = models.AutoField(primary_key=True)
    listingID = models.ForeignKey('listing.Listings', on_delete=models.CASCADE, related_name='images')
    imagePath = models.CharField(max_length=255)
    def __str__(self):
        return self.imagePath