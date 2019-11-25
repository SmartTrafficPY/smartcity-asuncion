from django.contrib import admin

from .models import UcarpoolingProfile


class UcarpoolingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UcarpoolingProfile, UcarpoolingProfileAdmin)
