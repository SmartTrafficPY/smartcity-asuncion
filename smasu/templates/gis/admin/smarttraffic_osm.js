{% extends "gis/admin/openlayers.js" %}
{% load geo_settings %}
{% block base_layer %}

new OpenLayers.Layer.OSM({% osm_layer_parameters %});

{% endblock %}
