from django.urls import include, path
from rest_framework import routers
from sp_lots.views import LotsExtra

from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

router = routers.DefaultRouter()
router.register("lots", views.LotsView)
router.register("spots", views.SpotsView)

urlpatterns = [path("", include(router.urls)), path("spots_of/<str:name>/", LotsExtra.as_view())]
