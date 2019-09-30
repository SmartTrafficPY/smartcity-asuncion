from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MovementType(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SmartMovingProfile(models.Model):
    FEMALE = "F"
    MALE = "M"

    SEX_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=16, choices=SEX_CHOICES)
    type_movement = models.ForeignKey(MovementType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
