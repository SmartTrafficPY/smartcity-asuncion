from django.contrib import admin
from uccarpool.models import Carpool, CarpoolRating, ItineraryRoute, RequestCarpool, UserItinerary

admin.site.register(UserItinerary)
admin.site.register(ItineraryRoute)
admin.site.register(Carpool)
admin.site.register(RequestCarpool)
admin.site.register(CarpoolRating)
