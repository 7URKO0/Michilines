var mapElement = document.getElementById('map');
var latitud = parseFloat(mapElement.getAttribute('data-latitud'));
var longitud = parseFloat(mapElement.getAttribute('data-longitud'));

// Log para verificar las coordenadas
console.log("Latitud:", latitud, "Longitud:", longitud);

// Verifica que las coordenadas sean válidas
if (!isNaN(latitud) && !isNaN(longitud)) {
    var map = L.map('map').setView([latitud, longitud], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);
    L.marker([latitud, longitud]).addTo(map)
        .bindPopup('Ubicación registrada de la mascota')
        .openPopup();
} else {
    console.error("Latitud o longitud inválidas.");
    alert("No se puede cargar el mapa debido a datos de ubicación inválidos.");
}
