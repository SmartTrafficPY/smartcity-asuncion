"""
This module contains all the models representing itinerary aspects of carpooling.

"""
from django.db import models


class PersonalityTraitType(models.Model):
    """
    Types of personality traits with the according weight while carpooling.
    For example:
    - Sex
    - Is a smoker
    - Eloquence level
    - Political affiliation
    """

    personalityTraitType = models.CharField(max_length=32, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f"{self.personalityTraitType}"