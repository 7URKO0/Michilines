// Inicializa el mapa y lo centra en Buenos Aires
var map = L.map('map').setView([-34.6037, -58.3816], 11);

// Agrega el mapa de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Añade un marcador en el mapa
//L.marker([-34.6037, -58.3816]).addTo(map)
//    .openPopup();
//
//L.marker([-34.6176, -58.3680]).addTo(map)
//    .openPopup();   
//
//L.marker([-34.5873, -58.3963]).addTo(map)
//    .openPopup();   

// Elementos del DOM
var coordinatesDisplay = document.getElementById('coordinates');
var latitudeInput = document.getElementById('latitud');
var longitudeInput = document.getElementById('longitud');
var statusDisplay = document.getElementById('status');

// Variable para guardar las coordenadas seleccionadas
var selectedCoordinates = null;

// Variable para el marcador
var currentMarker = null;

// Evento para capturar clics en el mapa
map.on('click', function (e) {
    // Obtener las coordenadas
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Guardar las coordenadas seleccionadas
    selectedCoordinates = { lat, lng };

    // Actualizar el texto visible y los campos ocultos
    coordinatesDisplay.innerText = `Latitud: ${lat.toFixed(6)}, Longitud: ${lng.toFixed(6)}`;
    latitudeInput.value = lat;
    longitudeInput.value = lng;
    document.getElementById('latitud').value = lat.toFixed(6);
    document.getElementById('longitud').value = lng.toFixed(6);
    // Eliminar el marcador anterior, si existe
    if (currentMarker) {
        map.removeLayer(currentMarker);
    }

    // Crear un nuevo marcador en el mapa
    currentMarker = L.marker([lat, lng]).addTo(map);

    // Limpiar el estado anterior
    statusDisplay.innerText = '';
});




document.getElementById("formularioMascotaPerdida").addEventListener("submit", function (e) {
    const latitud = document.getElementById("latitud").value;
    const longitud = document.getElementById("longitud").value;
    if (!latitud || !longitud) {
        e.preventDefault(); // Evita el envío
        alert("Por favor selecciona una ubicación en el mapa.");
    }
});