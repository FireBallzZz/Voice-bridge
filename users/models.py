from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_govt = models.BooleanField(default=False)
    division = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    upazila = models.CharField(max_length=100, blank=True)
    govt_code = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


    nid_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)