from django.urls import include, path
from rest_framework.routers import DefaultRouter
from uccarpool import views as uccarpool_views
from ucusers import views as ucusers_views

app_name = "ucusers"


router = DefaultRouter()
router.register("users", ucusers_views.UserView)
router.register("itinerary", uccarpool_views.UserItineraryView)
router.register("carpool", uccarpool_views.CarpoolView)

urlpatterns = [
    path("", include(router.urls)),
    path("auth-token/", ucusers_views.obtain_auth_token),
]
