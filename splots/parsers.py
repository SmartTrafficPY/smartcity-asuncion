from smasu.parsers import GeoJSONParser

from .renderers import ParkingSpotGeoJSONRenderer


class ParkingLotGeoJSONParser(GeoJSONParser):
    renderer_class = ParkingSpotGeoJSONRenderer
    other_geometry_keys = {"center"}


class ParkingSpotGeoJSONParser(GeoJSONParser):
    renderer_class = ParkingSpotGeoJSONRenderer
    geometry_key = "polygon"
