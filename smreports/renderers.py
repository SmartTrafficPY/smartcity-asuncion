from smasu.renderers import GeoJSONRenderer


class ReportPoiGeoJSONRenderer(GeoJSONRenderer):
    geometry_field = "coordinates"
