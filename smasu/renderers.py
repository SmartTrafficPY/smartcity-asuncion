import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import renderers


class GeoJSONRenderer(renderers.JSONRenderer):
    geometry_field = "geometry"
    other_geometry_fields = set()
    media_type = "application/vnd.geo+json"
    format = "geojson"

    def _render_feature(self, feature):
        geometry = None
        properties = {}
        for key in feature:
            value = feature.get(key)
            if value is not None and key in {self.geometry_field} | self.other_geometry_fields:
                value = GEOSGeometry(value)
                if value:
                    value = json.loads(value.json)

            if key == self.geometry_field:
                geometry = value
            else:
                properties[key] = value

        return {"type": "Feature", "properties": properties, "geometry": geometry}

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            data = self._render_feature(data)

        else:
            geojson_features = []
            for feature in data:

                geojson_features.append(self._render_feature(feature))

            data = {"type": "FeatureCollection", "features": geojson_features}

        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
