from django.urls import include, path
from rest_framework import routers
from spusers.views import LoginView, ResetPassView, isLoggedView

from . import views

router = routers.DefaultRouter()
router.register("users", views.UserView)

urlpatterns = [
    path("isUserLogged/", isLoggedView.as_view()),
    path("loggin/", LoginView.as_view()),
    path("isReseteable/", ResetPassView.as_view()),
    path("", include(router.urls)),
]
