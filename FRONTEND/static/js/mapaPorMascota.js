// Inicializa el mapa
function initializeMap(latitud, longitud) {
    var map = L.map('map').setView([latitud, longitud], 11); // Centra el mapa en las coordenadas de la mascota

    // Agrega el mapa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Añadir un marcador en el mapa
    L.marker([latitud, longitud]).addTo(map)
        .openPopup();
}

// Obtener el div con id "map" y acceder a las coordenadas almacenadas en data-attributes
var mapElement = document.getElementById('map');
var latitud = parseFloat(mapElement.getAttribute('data-latitud'));
var longitud = parseFloat(mapElement.getAttribute('data-longitud'));

// Verificar si las coordenadas son válidas antes de inicializar el mapa
if (!isNaN(latitud) && !isNaN(longitud)) {
    initializeMap(latitud, longitud);
} else {
    console.error("Coordenadas no válidas");
}