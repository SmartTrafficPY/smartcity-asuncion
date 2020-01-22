from smasu.renderers import GeoJSONRenderer


class ParkingLotGeoJSONRenderer(GeoJSONRenderer):
    other_geometry_fields = {"center"}


class ParkingSpotGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "polygon"
