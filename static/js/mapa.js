// Inicializa el mapa y céntralo en una ubicación específica (por ejemplo, San Francisco)
var map = L.map('map').setView([37.7749, -122.4194], 13);

// Agrega el mapa de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Añade un marcador en el mapa
L.marker([37.7749, -122.4194]).addTo(map)
    .bindPopup('San Francisco')
    .openPopup();