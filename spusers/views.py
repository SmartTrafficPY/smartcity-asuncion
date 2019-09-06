from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from smasu.authentication import IsCreateView, IsListView, IsSameUser, IsSuperUserOrStaff, TokenAuthenticationInQuery

from .models import SmartParkingProfile
from .serializers import UserSerializer


def get_application_group():
    group, created = Group.objects.get_or_create(name="smartparking apps")
    return group


class IsSmartParkingApp(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return super().has_permission(request, view) and user.groups.filter(pk=get_application_group().pk).exists()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (
        IsSuperUserOrStaff
        | ((IsListView | IsCreateView) & IsSmartParkingApp)
        | (~(IsListView | IsCreateView) & IsSameUser),
    )


class ObtainAuthToken(views.ObtainAuthToken):
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | IsSmartParkingApp,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        try:
            SmartParkingProfile.objects.get(user=user)
        except SmartParkingProfile.DoesNotExist:
            raise PermissionDenied

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "url": reverse("user-detail", args=[user.pk], request=request)})


obtain_auth_token = ObtainAuthToken.as_view()
