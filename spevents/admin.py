from django.contrib import admin

from .models import Events


class EventsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Events, EventsAdmin)
