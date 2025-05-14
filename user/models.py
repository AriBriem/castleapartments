from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone




# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email required")
        if not password:
            raise ValueError("Password required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    personal_id = models.CharField(max_length=255)
    postcode = models.ForeignKey('listing.Postcodes', on_delete=models.CASCADE)
    country = models.ForeignKey('user.Country', on_delete=models.CASCADE)
    profile_image_path = models.ImageField(upload_to="img/profilepics/", default="img/profilepics/default.jpg")
    cover_image_path = models.ImageField(upload_to="img/coverimages/", default="img/coverimages/default.jpg")
    register_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class SellerProfile(models.Model):
    user = models.OneToOneField('user.Users', on_delete=models.CASCADE)
    logo_path = models.ImageField(upload_to="img/logos/")
    bio = models.TextField()
    is_company = models.BooleanField()

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name