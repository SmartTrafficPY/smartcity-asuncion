from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# https://docs.djangoproject.com/en/2.2/topics/http/urls/

urlpatterns = [
    path('perfiles/all', views.ProfileList.as_view()),
    path('perfiles/<int:id>/', views.ProfilesCRUD.as_view()),
    path('perfiles/', views.ProfilesCRUD.as_view()),
]
