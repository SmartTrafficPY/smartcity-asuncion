import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnList


class GeoJSONRenderer(renderers.JSONRenderer):
    geometry_field = "geometry"
    media_type = "application/vnd.geo+json"
    format = "geojson"

    def _render_feature(self, feature):
        geometry = None
        properties = {}
        for key in feature:
            if key == self.geometry_field:
                geometry = GEOSGeometry(feature.get(self.geometry_field))
                if geometry:
                    geometry = json.loads(geometry.json)
            else:
                properties[key] = feature[key]
        return {"type": "Feature", "properties": properties, "geometry": geometry}

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            geojson_features = []
            for feature in data:

                geojson_features.append(self._render_feature(feature))

            data = {"type": "FeatureCollection", "features": geojson_features}

            # return smart_text(json.dumps(geojson_data)).encode(self.charset)
        else:
            data = self._render_feature(data)
            # return smart_text(json.dumps(self._render_feature(data))).encode(self.charset)

        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
