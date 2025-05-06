from django.db import models

from listing.models import Postcodes


# Create your models here.

class Users(models.Model):
    userID = models.IntegerField(primary_key=True)
    name = models.CharField()
    email = models.CharField()
    phoneNumber = models.CharField()
    password = models.CharField()
    address = models.CharField()
    personalID = models.CharField()
    postcode = models.ForeignKey(Postcodes, on_delete=models.CASCADE)
    country = models.CharField()
    profileImagePath = models.CharField()
    coverImagePath = models.CharField()
    registerDate = models.DateTimeField()
    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    userID = models.ForeignKey(Users, primary_key=True, on_delete=models.CASCADE)
    logoPath = models.CharField()
    bio = models.TextField()
    isCompany = models.BooleanField()