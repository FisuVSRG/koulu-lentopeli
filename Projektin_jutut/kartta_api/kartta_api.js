// Function to initialize a Leaflet map
function createLeafletMap(elementId, coordinates, zoomLevel = 5) {
    const map = L.map(elementId).setView(coordinates, zoomLevel);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Optional: Add a marker to the center of the map
    L.marker(coordinates).addTo(map);
}

// Initialize maps
createLeafletMap('map-left', [37.7749, -122.4194], 5); // San Francisco
createLeafletMap('map-right', [48.8566, 2.3522], 5);   // Paris
