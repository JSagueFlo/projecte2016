var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng },
        zoom: 17,
        scrollwheel: false,
        disableDefaultUI: true,
        draggable: false,
        styles:[{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#e0efef"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":100},{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"on"},{"lightness":700}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#80cbc4"}]}]
    });

    var marker = new google.maps.Marker({
        position: { lat: lat, lng: lng },
        map: map,
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        cursor: 'default'
    });
}
