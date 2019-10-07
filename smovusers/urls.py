from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register("users", views.UserView)

urlpatterns = [path("", include(router.urls)), path("auth-token/", views.obtain_auth_token)]
