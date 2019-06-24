from django.http import HttpResponse
from django.http import Http404
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from . serializer import perfilSerializers
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from . models import Perfil_SmartParking

import datetime

# DOCS:
# https://docs.djangoproject.com/en/2.2/topics/http/views/
# https://docs.djangoproject.com/en/2.2/topics/http/decorators/
# https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/
# REST_FRAMEWORK:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views

@api_view(['GET'])
@require_http_methods(["GET"])
def get_profile_by_id(request, id):
    try:
        obj = Perfil_SmartParking.objects.get(pk=id)
        data = perfilSerializers(obj)
    except Perfil_SmartParking.DoesNotExist:
        raise Http404("No profile matches the given query.")
    return Response(data.data, content_type='application/json')

@csrf_exempt
@api_view(['POST'])
@require_http_methods(["POST"])
# Need to do more control... null,etc
def post_profile_add(request):
    # if not exist that alias Profile, you can insert it in the DB...
    # query = Perfil_SmartParking.objects.get(alias=request.POST.get("alias"))
    # if query is None:
        # create the new one...
        query_insert = Perfil_SmartParking(password=request.data.get('password'), alias=request.data.get('alias'),
                                           created_at=current_datetime(), updated_at=current_datetime())
        query_insert.save()
        return HttpResponse("New profile created", status=200)
    # else:
        return HttpResponse("User profile already exists", status=500)

# #Missing DELETE and UPDATE...
# #by alias...
# @require_http_methods(["DELETE", "UPDATE"])
# def profile_change(request):
#     if request.method == "DELETE":
#
#     else:
#
#     #if not exist that alias Profile, you can insert it in the DB...
#     query_get = Perfil_SmartParking.objects.get(alias = request.body.alias)
#     if query_get is None:
#
#         return HttpResponse("New profile created", status=200)
#     else:
#         return HttpResponse("User profile already exists", status=500)


def current_datetime():
    now = datetime.datetime.now()
    return now
