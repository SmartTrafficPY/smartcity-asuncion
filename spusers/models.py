from django.contrib.auth.models import User
from django.db import models


class SmartParkingProfile(models.Model):

    FEMALE = "F"
    MALE = "M"
    SEX_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=16, choices=SEX_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
