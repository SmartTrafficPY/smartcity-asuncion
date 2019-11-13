"""
This module contains all the models representing the human-profile aspects of Ucarpooling system
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


class PersonalityTrait(models.Model):
    """
    Value of a specific personality trait.
    For example:
    - Sex -> M
    - Is a smoker -> No
    """

    personalityTraitType = models.ForeignKey(PersonalityTraitType, on_delete=models.CASCADE, null=False)
    personalityTraitValue = models.CharField(max_length=64, null=False, blank=False)

    "To avoid repeated rows, the combination of personalityTraitType & personalityTraitValue is unique."
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['personalityTraitType', 'personalityTraitValue'],
                                    name='unique_personality_and_value'),
        ]

    def __str__(self):
        return f"{self.personalityTraitValue}({self.personalityTraitType})"


class Person(models.Model):
    """
    Representation of a study subject.
    """

    personId = models.CharField(max_length=256, null=False, blank=False)
    personalityTraits = models.ManyToManyField(PersonalityTrait)

    "Every subject is unique, so in addition to the primary key, every personId must be unique ."
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['personId'], name='unique_person_id'),
        ]

    def __str__(self):
        return f"{self.personId}"
