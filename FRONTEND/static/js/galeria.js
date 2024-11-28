function filterGalleryBySelect() {
    // Captura de elementos una vez
    const category = document.getElementById('categorySelect').value;
    const items = Array.from(document.querySelectorAll('.gallery-item')); // Convertir a array para más flexibilidad
    let visibleCount = 0; // Contador para elementos visibles
  
    items.forEach(item => {
        if (category === 'all' || item.classList.contains(category)) {
            item.style.display = 'block'; // Mostrar el elemento
            visibleCount++;
        } else {
            item.style.display = 'none'; // Ocultar el elemento
        }
    });
  
    // Mostrar un mensaje si no hay elementos visibles
    const galleryContainer = document.getElementById('gallery-container');
    const noResultsMessageId = 'no-results-message';
    let noResultsMessage = document.getElementById(noResultsMessageId);
  
    if (visibleCount === 0) {
        if (!noResultsMessage) {
            noResultsMessage = document.createElement('p');
            noResultsMessage.id = noResultsMessageId;
            noResultsMessage.textContent = 'No hay mascotas en esta categoría.';
            galleryContainer.appendChild(noResultsMessage);
        }
    } else {
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }
  }
  