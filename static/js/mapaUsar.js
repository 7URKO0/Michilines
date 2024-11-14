// This example adds a marker to indicate the position of Bondi Beach in Sydney,
    // Australia.
    function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: {
            lat: 40.645037,
            lng: -73.880224
          },
        });
  
        var image = 'imagenes/maps-and-flags.png';
        var beachMarker = new google.maps.Marker({
          position: {
            lat: 40.645037,
            lng: -73.880224
          },
          map: map,
          icon: image
        });
      }
  
   