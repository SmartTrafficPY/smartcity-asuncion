from django.urls import include, path
from rest_framework import routers
from smreports import views as smreports_views

from . import views

router = routers.SimpleRouter()
router.register("users", views.UserView)
router.register("reports", smreports_views.PoiReportView)
router.register("statusupdates", smreports_views.StatusUpdatePoiView)

urlpatterns = [path("", include(router.urls)), path("auth-token/", views.obtain_auth_token)]
