from django.test import TestCase
from ucusers.models import PersonalityTraitType, PersonalityTrait

# Create your tests here.


class ModelTests(TestCase):
    """ Test suite for creating all user related models succesfully """

    def test_create_personality_trait_type_successful(self):
        """ Test if it can create a new PersonalityTraitType succesfully"""
        personalityTraitType = 'Afiliacion Politica'
        weight = 6.66
        var_personality_trait_type = PersonalityTraitType.objects.create(
            personalityTraitType=personalityTraitType,
            weight=weight
        )

        self.assertEqual(var_personality_trait_type.personalityTraitType, personalityTraitType)
        self.assertEqual(var_personality_trait_type.weight, weight)

    def test_create_personality_trait_successful(self):
        """ Test if it can create a new PersonalityTrait succesfully"""

        # First,create a new personality trait type
        var_personality_trait_type = PersonalityTraitType.objects.create(
            personalityTraitType='Afiliacion Futbolistica',
            weight=6.66
        )

        var_personality_trait = PersonalityTrait.objects.create(
            personalityTraitType=var_personality_trait_type,
            personalityTraitValue='Olimpia'
        )

        self.assertEqual(var_personality_trait.personalityTraitType, var_personality_trait_type)
        self.assertEqual(var_personality_trait.personalityTraitValue, 'Olimpia')


'''
    def test_create_person_successful(self):
        """ Test if it can create a new Person succesfully"""
        personId='af65gh8'

        # First,create a new personality trait type
        var_personality_trait_type = PersonalityTraitType.objects.create(
            personalityTraitType='Afiliacion Futbolistica',
            weight=6.66
        )

        #Second, create a personality trait
        var_personality_trait = PersonalityTrait.objects.create(
            personalityTraitType=var_personality_trait_type,
            personalityTraitValue='Olimpia'
        )

        #Third, create a person object
        var_person = Person.objects.create(
            personId=personId,
        )

        var_person.personalityTraits.add(var_personality_trait)


        self.assertEqual(var_person.personId, personId)
        self.assertEqual(var_person.personalityTraits, var_personality_trait)
'''
