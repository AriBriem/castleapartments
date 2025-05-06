from django.db import models

# Create your models here.

class Postcodes(models.Model):
    postcode = models.IntegerField(primary_key=True)
    country = models.CharField()
    def __str__(self):
        return self.postcode


class Listings(models.Model):
    listingID = models.IntegerField(primary_key=True)
    typeID = models.ForeignKey(Type, on_delete=models.CASCADE)
    sellerID = models.ForeignKey(Seller)
    address = models.CharField()
    sqrMeters = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    postcode = models.ForeignKey(Postcodes, on_delete=models.CASCADE)
    description = models.TextField()
    thumbnailPath = models.CharField()
    postDate = models.DateTimeField()

    def __str__(self):
        return self.listingID
