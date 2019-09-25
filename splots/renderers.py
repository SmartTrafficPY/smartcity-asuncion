from smasu.renderers import GeoJSONRenderer


class ParkingLotGeoJSONRenderer(GeoJSONRenderer):
    other_geometry_fields = {"center"}
    geometry_field = "gateway"


class ParkingSpotGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "polygon"
