from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'ucusers'


router = DefaultRouter()
router.register("users", views.UserView)


urlpatterns = [
    path("", include(router.urls)),
    path("auth-token/", views.obtain_auth_token)
]
