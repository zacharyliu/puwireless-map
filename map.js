var map;

function initMap() {
  // $.when($.get("bandwidth.csv"), $.get("core-87-locations.csv")).then(function (bandwidth, locations) {
  //   console.log(Papa.parse(bandwidth));
  //   console.log(locations);
  // });

  var heatmapData = [];

  Papa.parse("bandwidth.csv", {
    header: true,
    download: true,
    complete: function(bandwidth) {
      Papa.parse("core-87-locations.csv", {
        header: true,
        download: true,
        complete: function(locations) {
          var latlng = {};
          for (var i=0; i<locations.data.length; i++) {
            if (locations.data[i].lat) {
              latlng[locations.data[i]["interface"]] = new google.maps.LatLng(locations.data[i].lat, locations.data[i].lon);
            }
          }
          for (var i=0; i<bandwidth.data.length; i++) {
            if (latlng[bandwidth.data[i].interface]) {
              var weight = parseFloat(bandwidth.data[i].in) + parseFloat(bandwidth.data[i].out);
              if (!isNaN(weight)) {
                heatmapData.push({location: latlng[bandwidth.data[i].interface], weight: weight});
              }
            }
          }

          console.log(heatmapData);

          var heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmapData,
            radius: 0.0005,
            dissipating: false
          });
          heatmap.setMap(map);
        }
      });
    }
  });

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.3449003, lng: -74.6536822}, // Center on Princeton University
    zoom: 16
  });
}
