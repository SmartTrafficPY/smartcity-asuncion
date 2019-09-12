import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import exceptions, parsers
from smasu.renderers import GeoJSONRenderer


class GeoJSONParser(parsers.JSONParser):
    """
    Parses GeoJSON-serialized data.
    """

    media_type = "application/vnd.geo+json"
    renderer_class = GeoJSONRenderer
    geometry_key = "geometry"

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

        json_obj = {self.geometry_key: GEOSGeometry(json.dumps(geojson_obj.get("geometry"))).ewkt}

        for prop, value in geojson_obj.get("properties", {}).items():
            json_obj[prop] = value

        return json_obj
