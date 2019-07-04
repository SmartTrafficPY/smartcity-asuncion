from django.urls import path

from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

urlpatterns = [
    path("profiles/all", views.ProfileList.as_view()),
    path("profiles/login", views.ProfileLogin.as_view()),
    path("profiles/<int:id>/", views.ProfilesCRUD.as_view()),
    path("profiles/", views.ProfilesCRUD.as_view()),
]
