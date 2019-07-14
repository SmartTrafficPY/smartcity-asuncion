import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework import authentication, permissions
from .models import Sp_profiles
from .serializer import ProfileSerializers

# DOCS:
# https://docs.djangoproject.com/en/2.2/topics/http/views/
# https://docs.djangoproject.com/en/2.2/topics/http/decorators/
# https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/
# REST_FRAMEWORK:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views


class ProfileList(APIView):
    # Class view for Return List types of responses...

    def get(self, request, format=None):
        profile_sp = Sp_profiles.objects.all()
        serializer = ProfileSerializers(profile_sp, many=True)
        return Response(serializer.data)


class ProfileLogin(APIView):
    """
    Here we should recieve the user credentials, for making the login
    IF match, return the id, if NOT message
    """

    def post(self, request, format=None):
        try:
            profile_sp = Sp_profiles.objects.get(
                alias=request.data.get("alias"), password=request.data.get("password")
            )
        except Sp_profiles.DoesNotExist:
            return Response("This profile does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(ProfileSerializers(profile_sp).data)


class ProfilesCRUD(APIView):
    """
    Set Create, Read, Update and Delete services of SmartParking users profile
    View to list all users in the system.

    * Should requires token authentication.
    * Only some users should able to access this view.
    """

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get_object_id(self, id):
        try:
            return Sp_profiles.objects.get(id=id)
        except Sp_profiles.DoesNotExist:
            raise Http404

    def get_object_alias(self, alias):
        try:
            return Sp_profiles.objects.get(alias=alias)
        except Sp_profiles.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        perfil_sp = self.get_object_id(id)
        serializer = ProfileSerializers(perfil_sp)
        return Response(serializer.data)

    def post(self, request, format=None):
        # if not exist that alias in another profile, you can insert it in the DB...
        try:
            Sp_profiles.objects.get(alias=request.data.get("alias"))
        except Sp_profiles.DoesNotExist:
            query_insert = Sp_profiles(
                password=request.data.get("password"),
                alias=request.data.get("alias"),
                age=request.data.get("age"),
                sex=request.data.get("sex"),
                created_at=current_datetime(),
                updated_at=current_datetime(),
            )
            query_insert.save()
            return Response(ProfileSerializers(query_insert).data, status=status.HTTP_201_CREATED)
        else:
            return Response("This profile already exists", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that alias Profile, update else conflict...
        # for now let you to update the password...
        try:
            perfil_sp = Sp_profiles.objects.get(alias=request.data.get("alias"))
        except Sp_profiles.DoesNotExist:
            return Response("This alias profile does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            perfil_sp.password = request.data.get("password")
            perfil_sp.updated_at = current_datetime()
            perfil_sp.save()
            return Response(request.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, format=None):
        profile_sp = self.get_object_id(id)
        profile_sp.delete()
        return Response(status=status.HTTP_200_OK)


def current_datetime():
    now = datetime.datetime.now()
    return now
