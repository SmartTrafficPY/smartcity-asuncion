from django.contrib import admin

from .models import MovementType, SmartMovingProfile

# Register your models here.


class SmartMovingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(SmartMovingProfile, SmartMovingProfileAdmin)


class SmartMovingMovementType(admin.ModelAdmin):
    pass


admin.site.register(MovementType, SmartMovingMovementType)
