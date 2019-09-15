from smasu.parsers import GeoJSONParser

from .renderers import EventGeoJSONRenderer


class EventGeoJSONParser(GeoJSONParser):
    renderer_class = EventGeoJSONRenderer
    geometry_key = "position"
