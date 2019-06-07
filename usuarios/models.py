from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255)
    userlastname = models.CharField(max_length=255)
    userage = models.IntegerField()

    def __str__(self):
        return self.username