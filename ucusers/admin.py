from django.contrib import admin
from ucusers.models import Person, PersonalityTrait, PersonalityTraitType

admin.site.register(Person)
admin.site.register(PersonalityTrait)
admin.site.register(PersonalityTraitType)