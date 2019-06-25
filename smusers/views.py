from rest_framework import viewsets

from .models import User
from .serializer import userSerializers


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers
