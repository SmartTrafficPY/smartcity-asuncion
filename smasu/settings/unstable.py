import os

from .base import *  # noqa

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = [x.strip() for x in os.environ["ALLOWED_HOSTS"].split(",")]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "smarttraffic",
        "USER": "smarttraffic",
        "PASSWORD": os.environ["PG_PASSWORD"],
        "HOST": "postgres",
        "PORT": "5432",
    }
}

NEARBY_SPOTS_DEFAULT_DISTANCE = os.getenv("NEARBY_SPOTS_DEFAULT_DISTANCE", NEARBY_SPOTS_DEFAULT_DISTANCE)

spot_state_expires_in_hours = os.getenv("SPOT_STATE_EXPIRATION_TIME")
if spot_state_expires_in_hours:
    SPOT_STATE_EXPIRATION_TIME = timedelta(hours=int(spot_state_expires_in_hours))

OSM_LAYER_NAME = os.getenv("OSM_LAYER_NAME")
OSM_LAYER_URL_PATTERN = os.getenv("OSM_LAYER_URL_PATTERN")
