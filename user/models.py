from django.db import models




# Create your models here.

class Users(models.Model):
    userID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    personalID = models.CharField(max_length=255)
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    profileImagePath = models.CharField(max_length=255)
    coverImagePath = models.CharField(max_length=255)
    registerDate = models.DateTimeField()
    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    userID = models.ForeignKey('user.Users', primary_key=True, on_delete=models.CASCADE)
    logoPath = models.CharField(max_length=255)
    bio = models.TextField()
    isCompany = models.BooleanField()