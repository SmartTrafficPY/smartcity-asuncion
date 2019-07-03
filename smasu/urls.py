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

# from rest_framework.urlpatterns import format_suffic_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    # Here should go to all 3 cases of study... and a basic common one
    path("api/", include("smusers.urls")),
    path("health/", include("smhealth.urls")),
    path("smartparking/", include("sp_lots.urls")),
]
