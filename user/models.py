from django.db import models




# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    personal_id = models.CharField(max_length=255)
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    profile_image_path = models.ImageField(upload_to="img/profilepics/")
    cover_image_path = models.ImageField(upload_to="img/coverimages/")
    register_date = models.DateTimeField()
    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    user = models.OneToOneField('user.Users', on_delete=models.CASCADE)
    logo_path = models.ImageField(upload_to="img/logos/")
    bio = models.TextField()
    is_company = models.BooleanField()

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name