from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register("events", views.EventViewSet)

urlpatterns = [path("services/", include(router.urls))]
