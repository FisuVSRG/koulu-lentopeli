let mapOptions = {
    center: [59.3327, 18.0656],
    zoom: 5
};

let map = new L.map('map', mapOptions);

let layer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
map.addLayer(layer);

let marker = new L.Marker([59.3327, 18.0656]); // tätä muokataan kun haetaan
marker.addTo(map);