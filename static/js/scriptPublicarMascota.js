document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formularioMascotaPerdida');
    
    formulario.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const mascotaData = {
            nombre: document.getElementById('nombreMascota').value,
            edad: document.getElementById('edadMascota').value,
            especie: document.getElementById('especie').value,
            condicion: document.getElementById('condicion').value,
            descripcion: document.getElementById('descripcion').value,
            fechaPerdida: document.getElementById('fechaPerdida').value,
            ubicacion: null //agregar el mapa
        };


        // falta agrear toda la funcionalidad de las apis(agregar los datos a las apis)
        // manejar tema de la foto
        // validar todo el formulario
        // y no se que mas pero falta

    }); 
}); 