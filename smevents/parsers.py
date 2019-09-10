from smasu.parsers import GeoJSONParser

from .renderers import EventGeoJSONRenderer


class EventGeoJSONParser(GeoJSONParser):
    geometry_key = "position"
    renderer_class = EventGeoJSONRenderer
