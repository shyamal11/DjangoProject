from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UserDetails(models.Model):
    Username = models.CharField(max_length=50 , primary_key=True)
    Email = models.EmailField(max_length=25, unique=True)
    Password = models.CharField(max_length=12, blank=True)


    




