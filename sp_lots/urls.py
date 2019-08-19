from django.urls import include, path
from rest_framework import routers
from sp_lots.views import LotsView, SpotsView

from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

router = routers.DefaultRouter()
router.register("lots", views.LotsView)
router.register("spots", views.SpotsView)

urlpatterns = [
    path("spots_of/<int:pk>/", SpotsView.as_view({"get": "list"})),
    path("lots/all/", LotsView.as_view({"get": "list"})),
    path("", include(router.urls)),
]
