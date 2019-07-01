from django.urls import path

from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

urlpatterns = [
    path("lots/all", views.LotsList.as_view()),
    path("lots/<int:id>/", views.LotsCRUD.as_view()),
    path("lots/", views.LotsCRUD.as_view()),
    path("spots/all", views.SpotsList.as_view()),
    path("spots/<int:id>/", views.SpotsCRUD.as_view()),
    path("spots/", views.SpotsCRUD.as_view()),
]
