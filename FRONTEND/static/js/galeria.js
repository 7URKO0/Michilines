function filterGalleryBySelect() {
  const category = document.getElementById('categorySelect').value;
  const items = document.querySelectorAll('.gallery-item');

  items.forEach(item => {
      console.log(item);  
      if (category === 'all' || item.classList.contains(category)) {
          item.style.display = 'block';
      } else {
          item.style.display = 'none';
      }
  });
}
