
from rest_framework import viewsets, status
from . models import User
from . serializer import userSerializers

# Create your views here.

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers
