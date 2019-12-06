from django.contrib import admin
from uccarpool.models import Carpool, CarpoolItinerary, RequestCarpool, UserItinerary

admin.site.register(UserItinerary)
admin.site.register(CarpoolItinerary)
admin.site.register(Carpool)
admin.site.register(RequestCarpool)
