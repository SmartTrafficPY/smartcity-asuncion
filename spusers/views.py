from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import UserSerializer

# from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)


class isLoggedView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, format=None):
        if request.user is not None:
            if request.user.is_authenticated and request.session:
                return Response(request.session, status=status.HTTP_200_OK)
            else:
                return Response(request.session, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(request.session, status=status.HTTP_404_UNAUTHORIZED)


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

    @method_decorator(csrf_protect)
    def get(self, request, format=None):
        return Response({}, status=status.HTTP_200_OK)


class ResetPassView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request, format=None):
        try:
            User.objects.get(
                username=request.data.get("username"),
                smartparkingprofile__birth_date=request.data.get("birth_date"),
                smartparkingprofile__sex=request.data.get("sex"),
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_202_ACCEPTED)
