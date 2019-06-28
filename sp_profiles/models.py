from django.db import models


# Create your models here.
class Sp_profiles(models.Model):
    # Not follow the anonymity that we want to pursuit...
    # name = models.CharField(max_length=50)
    # lastname = models.CharField(max_length=50)
    # email = models.CharField(max_length=150)
    password = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alias