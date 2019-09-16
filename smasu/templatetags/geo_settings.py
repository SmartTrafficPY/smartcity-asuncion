from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def osm_layer_parameters():
    parameters = '"{}"'.format(settings.OSM_LAYER_NAME or "OpenStreetMap (Mapnik)")
    if settings.OSM_LAYER_URL_PATTERN:
        parameters = f'{parameters}, "{settings.OSM_LAYER_URL_PATTERN}"'
    return mark_safe(parameters)
