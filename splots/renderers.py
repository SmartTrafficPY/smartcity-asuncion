from smasu.renderers import GeoJSONRenderer


class SpotGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "polygon"
