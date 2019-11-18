from smasu.parsers import GeoJSONParser

from .renderers import ReportPoiGeoJSONRenderer


class ReportPoiGeoJSONParser(GeoJSONParser):
    renderer_class = ReportPoiGeoJSONRenderer
    geometry_key = "coordinates_poi"
