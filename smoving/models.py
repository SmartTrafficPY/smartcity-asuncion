from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class MovementType(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    FEMALE = "F"
    MALE = "M"
    SEX_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=16, choices=SEX_CHOICES)
    type_movement = models.ForeignKey(MovementType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Report(models.Model):
    latitude = models.DecimalField(max_digits=50, decimal_places=50)
    longitude = models.DecimalField(max_digits=50, decimal_places=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # the user id that create the POI
    created = models.DateTimeField(auto_now_add=True)  # when was created
    modified = models.DateTimeField(auto_now=True)


class ReportType(models.Model):
    image = models.TextField()


class Contribution(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    truthness = models.BooleanField()
