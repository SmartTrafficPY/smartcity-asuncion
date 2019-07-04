from django.db import models


# Create your models here.
class Sp_profiles(models.Model):
    """
    We should add some way to set back de password...
    """

    # Not follow the anonymity that we want to pursuit...
    # name = models.CharField(max_length=50)
    # lastname = models.CharField(max_length=50)
    # email = models.CharField(max_length=150)
    SEX_CHOICES = (("Male", "M"), ("Female", "F"))
    password = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alias
