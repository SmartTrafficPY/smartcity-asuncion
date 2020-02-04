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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from smevents.views import EventViewSet

from . import views

admin.site.site_header = settings.PLATFORM_NAME

router = routers.DefaultRouter()
router.register("events", EventViewSet)

entities_patterns = (
    [
        path("users/<int:pk>/", views.empty, name="users"),
        path("smartparking/event_types/<slug:pk>/", views.empty, name="smartparking_event_types"),
        path("smartmoving/event_types/<slug:pk>", views.empty, name="smartmoving_event_types"),
    ],
    "entities",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("smhealth.urls")),
    path("entities/", include(entities_patterns)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include(router.urls)),
    path("api/smartparking/", include("spusers.urls")),
    path("api/smartmoving/", include("smovusers.urls")),
]
