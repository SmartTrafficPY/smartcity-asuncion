from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import UserSerializer

# from rest_framework.decorators import detail_route


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)


class isLoggedView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, format=None):
        if request.user.is_authenticated:
            return Response(request.session, status=status.HTTP_200_OK)
        else:
            return Response(UserSerializer(request.user).data, status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        current_pass = data.get("current_pass", None)
        new_pass = data.get("new_pass", None)
        user = authenticate(username=request.user.username, password=current_pass)
        if user is not None:
            user.password = make_password(new_pass)
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request, format=None):
        data = request.data

        username = data.get("username", None)
        password = data.get("password", None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)
