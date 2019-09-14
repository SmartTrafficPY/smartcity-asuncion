"""smasu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

entities_patterns = (
    [
        path("users/<int:pk>/", views.empty, name="users"),
        path("smartparking/event_types/<slug:pk>/", views.empty, name="smartparking_event_types"),
    ],
    "entities",
)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("health/", include("smhealth.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("smevents.urls")),
    path("entities/", include(entities_patterns)),
    path("smartparking/", include("spusers.urls")),
    path("smartparking/", include("splots.urls")),
]
