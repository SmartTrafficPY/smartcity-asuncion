from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.username
