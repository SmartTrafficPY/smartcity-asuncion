{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}

// source.setTileLoadFunction(function(tile, src) {
//   var xhr = new XMLHttpRequest();
//   xhr.responseType = 'blob';
//   xhr.addEventListener('loadend', function (evt) {
//     var data = this.response;
//     if (data !== undefined) {
//       tile.getImage().src = URL.createObjectURL(data);
//     } else {
//       tile.setState(TileState.ERROR);
//     }
//   });
//   xhr.addEventListener('error', function () {
//     tile.setState(TileState.ERROR);
//   });
//   xhr.open('GET', src);
//   xhr.send();
// });

// var old_issue = console.log;
// console.log = function() {
//    // Invoke the original method with an additional parameter
//    log.apply(console, [(new Date()).toString()].concat(arguments));
// };

new OpenLayers.Layer.OSM(
    "OpenStreetMap (Mapnik)",
    "https://smartparking0:phobicflower934@smarttraffic.com.py/tile/${z}/${x}/${y}.png",
    {
        // crossOriginKeyword: "anaonymous",
        // tileLoadFunction: function(tile, src) {
        //     var client = new XMLHttpRequest();
        //     client.open('GET', src);
        //     client.setRequestHeader('foo', 'bar');
        //     client.onload(function() {
        //         var data = 'data:image/png;base64,' + btoa(unescape(encodeURIComponent(this.responseText)));
        //         tile.getImage().src = data;
        //     });
        //     client.send();
        // },
        tileOptions: {
            tileLoadFunction: function(tile, src) {
                return;
                var xhr = new XMLHttpRequest();
                xhr.responseType = 'blob';
                xhr.addEventListener('loadend', function (evt) {
                    var data = this.response;
                    if (data !== undefined) {
                        tile.getImage().src = URL.createObjectURL(data)+'11';
                    } else {
                        tile.setState(TileState.ERROR);
                    }
                });
                xhr.addEventListener('error', function () {
                    tile.setState(TileState.ERROR);
                });
                xhr.open('GET', src);
                xhr.setRequestHeader('X-Hello', 'Hola');
                xhr.send();
            },
        },
    });

{% endblock %}
