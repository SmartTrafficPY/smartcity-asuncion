from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class UcarpoolingProfile(models.Model):

    SEX_MALE = "M"
    SEX_FEMALE = "F"
    SEX_CHOICES = ((SEX_MALE, "Male"), (SEX_FEMALE, "Female"))

    MUSIC_GENRE_NO_PREFERENCE = "NO_PREF"
    MUSIC_GENRE_SILENCE = "SILENCE"
    MUSIC_GENRE_POP = "POP"
    MUSIC_GENRE_TECHNO = "TECHNO"
    MUSIC_GENRE_ELECTRONIC = "ELECTRONIC"
    MUSIC_GENRE_ROCK = "ROCK"
    MUSIC_GENRE_METAL = "METAL"
    MUSIC_GENRE_RAP = "RAP"
    MUSIC_GENRE_REGGAE = "REGGAE"
    MUSIC_GENRE_CUMBIA = "CUMBIA"
    MUSIC_GENRE_REGGAETON = "REGGAETON"
    MUSIC_GENRE_TRAP = "TRAP"
    MUSIC_GENRE_FUNK = "FUNK"
    MUSIC_GENRES = (
        (MUSIC_GENRE_NO_PREFERENCE, "No preference"),
        (MUSIC_GENRE_SILENCE, "I like silence"),
        (MUSIC_GENRE_POP, "Pop"),
        (MUSIC_GENRE_TECHNO, "Techno"),
        (MUSIC_GENRE_ELECTRONIC, "Electronic"),
        (MUSIC_GENRE_ROCK, "Rock"),
        (MUSIC_GENRE_METAL, "Metal"),
        (MUSIC_GENRE_RAP, "Rap"),
        (MUSIC_GENRE_REGGAE, "Reggae"),
        (MUSIC_GENRE_CUMBIA, "Cumbia"),
        (MUSIC_GENRE_REGGAETON, "Reggaeton"),
        (MUSIC_GENRE_TRAP, "Trap"),
        (MUSIC_GENRE_FUNK, "Funk"),
    )

    ELOQUENCE_LEVEL_LOW = 1
    ELOQUENCE_LEVEL_MEDIUM = 2
    ELOQUENCE_LEVEL_HIGH = 3
    ELOQUENCE_LEVELS = (
        (ELOQUENCE_LEVEL_LOW, "Introverted"),
        (ELOQUENCE_LEVEL_MEDIUM, "Medium"),
        (ELOQUENCE_LEVEL_HIGH, "Extroverted"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    sex = models.CharField(max_length=16, choices=SEX_CHOICES)
    smoker = models.BooleanField()
    musicTaste = ArrayField(models.CharField(max_length=15, blank=False, choices=MUSIC_GENRES), default=list,)
    eloquence_level = models.IntegerField(choices=ELOQUENCE_LEVELS, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
