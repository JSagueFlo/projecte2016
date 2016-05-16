var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng },
        zoom: 15,
        scrollwheel: false,
        disableDefaultUI: true,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP, //TERRAIN,SATELLITE,ROADMAP,HYBRID
        styles:[{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#e0efef"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":100},{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"on"},{"lightness":700}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#80cbc4"}]}]
    });
    for( var i = 0; i < boies.length; i++) {
        var marker = new google.maps.Marker({
            position: { lat: parseFloat(boies[i].lat), lng: parseFloat(boies[i].lng)},
            map: map,
            title: boies[i].location_name,
            icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            boia_id: data[i].pk
        });
        marker.addListener('click', function() {
            window.location.href = url + this.boia_id;
        });
    }
}
