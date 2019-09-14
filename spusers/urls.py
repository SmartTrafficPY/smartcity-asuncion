from django.urls import include, path
from rest_framework import routers
from splots import views as splots_views

from . import views

router = routers.SimpleRouter()
router.register("users", views.UserView)
router.register("lots", splots_views.ParkingLotView)
router.register("spots", splots_views.ParkingSpotView)

urlpatterns = [path("", include(router.urls)), path("auth-token/", views.obtain_auth_token)]
