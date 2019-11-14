import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import exceptions, parsers
from smasu.renderers import GeoJSONRenderer, NearbyGeoJSONRenderer


class GeoJSONParser(parsers.JSONParser):
    """
    Parses GeoJSON-serialized data.
    """

    media_type = "application/vnd.geo+json"
    renderer_class = GeoJSONRenderer
    geometry_key = "geometry"
    other_geometry_keys = set()

    @staticmethod
    def _parse_geometry(geometry_obj):
        if geometry_obj is None:
            return None
        return GEOSGeometry(json.dumps(geometry_obj)).ewkt

    def parse(self, stream, media_type=None, parser_context=None):
        geojson_obj = super().parse(stream, media_type=media_type, parser_context=parser_context)

        if geojson_obj is None:
            return None

        try:
            o_type = geojson_obj["type"]
        except KeyError:
            raise exceptions.ParseError("malformed geojson object")

        if o_type != "Feature":
            raise exceptions.ParseError("can only accept geojson objects of type 'Feature'")

        json_obj = {self.geometry_key: self._parse_geometry(geojson_obj.get("geometry"))}

        for prop, value in geojson_obj.get("properties", {}).items():
            if prop in self.other_geometry_keys:
                value = self._parse_geometry(value)
            json_obj[prop] = value

        return json_obj


class NearbyGeoJSONParser(GeoJSONParser):
    renderer_class = NearbyGeoJSONRenderer
    geometry_key = "point"
