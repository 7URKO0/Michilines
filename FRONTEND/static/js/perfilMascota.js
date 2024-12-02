document.addEventListener('DOMContentLoaded', () => {
    const botonesEliminar = document.querySelectorAll('.eliminar-btn');

    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', async (e) => {
            const idComentario = e.target.dataset.id;

            const confirmacion = confirm('¿Estás seguro de que deseas eliminar este comentario?');
            if (!confirmacion) return;

            try {
                const respuesta = await fetch(`/comentarios/${idComentario}`, { method: 'DELETE' });
                const resultado = await respuesta.json();

                if (respuesta.ok) {
                    alert(resultado.message);
                    location.reload(); // Recargar la página para reflejar los cambios
                } else {
                    alert(`Error: ${resultado.message}`);
                }
            } catch (error) {
                console.error('Error al eliminar el comentario:', error);
                alert('Ocurrió un error al intentar eliminar el comentario.');
            }
        });
    });
});
