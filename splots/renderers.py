from smasu.renderers import GeoJSONRenderer


class LotGeoJSONRenderer(GeoJSONRenderer):
    other_geometry_fields = {"center"}


class SpotGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "polygon"
