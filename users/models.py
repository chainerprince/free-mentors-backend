from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255,default="None")
    expertise = models.CharField(max_length=255,default="None")
    has_mentor_role = models.BooleanField(default=False)
    has_admin_role = models.BooleanField(default=False)