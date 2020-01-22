from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here


class NavigationRequest(models.Model):

    SCORE_CHOICES = zip(range(1, 6), range(1, 6))

    user_requested = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = PointField()
    destination = PointField()
    route = ArrayField(models.TextField(blank=True, null=True), default=list, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    finish_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    finished = models.BooleanField(null=False, help_text="true if user finished the navigation, false if didn't")
    score = models.IntegerField(choices=SCORE_CHOICES, null=True, help_text="1 lowest score, 5 highest score")
    report_severe = models.TextField(blank=True, null=True)
    report_light = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.score}"
