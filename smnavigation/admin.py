# Register your models here.
from django.contrib import admin

from .models import NavigationRequest


class NavigationRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(NavigationRequest, NavigationRequestAdmin)
