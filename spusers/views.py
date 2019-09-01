from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import TokenAuthenticationInQuery

from .models import SmartParkingProfile
from .serializer import UserSerializer


def get_application_group():
    group, created = Group.objects.get_or_create(name="smartparking apps")
    return group


class IsListView(BasePermission):
    def has_permission(self, request, view):
        return view.action == "list"


class IsSmartParkingApp(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return super().has_permission(request, view) and (
            user.is_superuser or user.is_staff or user.groups.filter(pk=get_application_group().pk).exists()
        )


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = ((IsListView & IsSmartParkingApp) | (~IsListView & IsAuthenticated),)


class ObtainAuthToken(views.ObtainAuthToken):
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSmartParkingApp,)

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
