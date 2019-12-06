"""
This module contains all the models representing scheduled trips of carpooling.
"""
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
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
    isDriver = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Itineraries"


class CarpoolItinerary(models.Model):
    """
    Since a carpool has a route consisting of geographical points, a stamped Geopoint with date and time is modeled.
    ...

    Attributes
    ----------
    itinerary : UserItinerary
        The itinerary of the driver of the carpool
    geopoints : ArrayField(PointField)
        Latitude and longitude of a point in a carpool's route
    timestamps : ArrayField(datetime)
        Date and time for which a carpool has been or will be in that geopoint
    """

    itinerary = models.ForeignKey(UserItinerary, on_delete=models.CASCADE, blank=True, null=True)
    geopoints = ArrayField(PointField(blank=True, null=True), default=list, blank=True, null=True)
    timestamps = ArrayField(models.DateTimeField(auto_now_add=False, blank=True, null=True), blank=True, null=True)

    class Meta:
        verbose_name_plural = "Carpool Itineraries"


class Carpool(models.Model):
    """
    Representative class of a carpool, with a driver and the respective poolers.
    ...

    Attributes
    ----------
    driver : Person
        Who is the driver
    pooler : Person
        A passanger that is part of the carpool
    carpoolItinerary : CarpoolItinerary
        To which CarpoolItinerary this carpool is assigned to
    """

    driver = models.ForeignKey(
        UcarpoolingProfile, on_delete=models.CASCADE, blank=True, null=True, related_name="driver"
    )
    poolers = models.ManyToManyField(UcarpoolingProfile, related_name="poolers")
    carpoolItinerary = models.ForeignKey(CarpoolItinerary, on_delete=models.CASCADE, blank=True, null=True)


class RequestCarpool(models.Model):
    """
    A request to be part of a carpool from a sender to a reciever
    ...

    Attributes
    ----------
    driver : Person
        Who is the driver
    pooler : Person
        A passanger that is part of the carpool
    carpoolItinerary : CarpoolItinerary
        To which CarpoolItinerary this carpool is assigned to
    """

    sender = models.ForeignKey(UcarpoolingProfile, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(UcarpoolingProfile, on_delete=models.CASCADE, related_name="recipient")
    subject = models.ForeignKey(Carpool, on_delete=models.CASCADE, blank=True, null=True)
