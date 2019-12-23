from smasu.renderers import GeoJSONRenderer


class EventGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "position"
