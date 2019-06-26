from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import authentication, permissions
from django.views.decorators.csrf import csrf_exempt
from . models import Perfil_SmartParking
from . serializer import perfilSerializers
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet


import datetime

# DOCS:
# https://docs.djangoproject.com/en/2.2/topics/http/views/
# https://docs.djangoproject.com/en/2.2/topics/http/decorators/
# https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/
# REST_FRAMEWORK:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views

class ProfileList(APIView):

    # Class view for Return List types of responses...

    def get(self, request, format=None):
        profile_sp = Perfil_SmartParking.objects.all()
        serializer = perfilSerializers(profile_sp, many=True)
        return Response(serializer.data)  

class ProfilesCRUD(APIView):
    """
    Set Create, Read, Update and Delete services of SmartParking users profile
    """
    """
    View to list all users in the system.

    * Should requires token authentication.
    * Only some users should able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get_object_id(self, id):
        try:
            return Perfil_SmartParking.objects.get(id=id)
        except Perfil_SmartParking.DoesNotExist:
            raise Http404

    def get_object_alias(self, alias):
        try:
            return Perfil_SmartParking.objects.get(alias=alias)
        except Perfil_SmartParking.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        perfil_sp = self.get_object_id(id)
        serializer = perfilSerializers(perfil_sp)
        return Response(serializer.data)

    def post(self, request, format=None):
        # if not exist that alias in another profile, you can insert it in the DB...
        try:
            perfil_sp = Perfil_SmartParking.objects.get(alias=request.data.get('alias'))
        except Perfil_SmartParking.DoesNotExist:
            query_insert = Perfil_SmartParking(password=request.POST.get('password'), alias=request.POST.get('alias'),
                                            created_at=current_datetime(), updated_at=current_datetime())
            query_insert.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response("This profile already exists", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that alias Profile, update else conflict...
        # for now let you to update the password...
        try:
            perfil_sp = Perfil_SmartParking.objects.get(alias=request.data.get('alias'))
        except Perfil_SmartParking.DoesNotExist:
            return Response("This alias profile does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            perfil_sp.password = request.data.get('password')
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
