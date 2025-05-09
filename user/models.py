from django.db import models




# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    personalID = models.CharField(max_length=255)
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    profileImagePath = models.ImageField(upload_to="img/profilepics/")
    coverImagePath = models.ImageField(upload_to="img/coverimages/")
    registerDate = models.DateTimeField()
    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    userID = models.OneToOneField('user.Users', on_delete=models.CASCADE)
    logoPath = models.ImageField(upload_to="img/logos/")
    bio = models.TextField()
    isCompany = models.BooleanField()

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name