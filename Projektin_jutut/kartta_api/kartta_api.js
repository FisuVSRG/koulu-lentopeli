function createLeafletMap(coordinates, zoomLevel = 5) {
  // Define map options with dynamic center based on coordinates
  let mapOptions = {
    center: coordinates,
    zoom: zoomLevel
  };

  // Create the map
  let map = new L.map('map', mapOptions);

  // Add the tile layer
  let layer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });
  map.addLayer(layer);

  // Add a marker to the center (optional, can be customized)
  let marker = new L.Marker(coordinates);
  marker.addTo(map);
}

createLeafletMap([35.6895, 139.6917], 10); // Tokyo coordinates with zoom level 10