from smasu.parsers import GeoJSONParser

from .renderers import ParkingSpotGeoJSONRenderer


class ParkingSpotGeoJSONParser(GeoJSONParser):
    geometry_key = "polygon"
    renderer_class = ParkingSpotGeoJSONRenderer
