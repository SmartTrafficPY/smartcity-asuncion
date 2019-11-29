"""
This module contains all the models representing scheduled trips of carpooling.
"""
from django.contrib.gis.db.models import PointField
from django.db import models
from ucusers.models import UcarpoolingProfile


class Itinerary(models.Model):
    """
    Abstract Class that represent the organization or schedule of ANY trip.
    """

    timeOfDeparture = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    timeOfArrival = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    origin = PointField(blank=True, null=True)
    destination = PointField(blank=True, null=True)

    class Meta:
        abstract = True


class UserItinerary(Itinerary):
    """
    Class that inherit from Itinerary, that represents the coordination of a
    single study subject for that day. Specifically when going to or coming from the institution in common studied.

    ...

    Attributes
    ----------
    isDriver : boolean
        If the subject is driving in a particular trip
    ucarpoolingProfile : UcarpoolingProfile
        The subject that this itinerary belongs to
    """

    ucarpoolingProfile = models.ForeignKey(UcarpoolingProfile, on_delete=models.CASCADE, blank=True, null=True)
    isDriver = models.BooleanField()

    class Meta:
        verbose_name_plural = "User Itineraries"
