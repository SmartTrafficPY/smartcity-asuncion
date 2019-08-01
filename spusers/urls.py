from django.urls import include, path
from rest_framework import routers
from spusers.views import ChangePasswordView, LoginView, LogoutView, isLoggedView

from . import views

router = routers.DefaultRouter()
router.register("users", views.UserView)

urlpatterns = [
    path("changePass/", ChangePasswordView.as_view()),
    path("isUserLogged/", isLoggedView.as_view()),
    path("loggin/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("", include(router.urls)),
]
