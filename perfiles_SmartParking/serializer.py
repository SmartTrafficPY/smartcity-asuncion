from rest_framework import serializers
from . models import Perfil_SmartParking

# https://docs.djangoproject.com/en/2.2/topics/serialization/

class perfilSerializers(serializers.ModelSerializer):

    class Meta:
        model = Perfil_SmartParking
        fields = '__all__'