from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializer import userSerializers


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers
