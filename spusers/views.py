from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import TokenAuthenticationInQuery

from .models import SmartParkingProfile
from .serializer import UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsAuthenticated,)


class ObtainAuthToken(views.ObtainAuthToken):
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        try:
            SmartParkingProfile.objects.get(user=user)
        except SmartParkingProfile.DoesNotExist:
            raise PermissionDenied

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


obtain_auth_token = ObtainAuthToken.as_view()
