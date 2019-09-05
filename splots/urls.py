from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("lots", views.ParkingLotView)
router.register("spots", views.ParkingSpotView)

urlpatterns = [path("", include(router.urls))]
