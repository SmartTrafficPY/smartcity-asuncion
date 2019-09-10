from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from smasu.models import Application


class Event(models.Model):
    application = models.ForeignKey(
        Application,
        related_name="events",
        on_delete=models.CASCADE,
        blank=False,
        help_text="The application that is sourcing the event.",
    )
    e_type = models.URLField(blank=False, db_index=True, help_text="The type of event.")
    agent = models.URLField(blank=True, db_index=True, help_text="Who is the main agent in the event.")
    position = PointField(blank=True, db_index=True, help_text="Sensor position at the instant the event takes place.")
    instant = models.DateTimeField(
        default=timezone.now, db_index=True, help_text="Point in time when the event occurs."
    )
    extra_information = JSONField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - App({self.application}), Type({self.e_type})"
