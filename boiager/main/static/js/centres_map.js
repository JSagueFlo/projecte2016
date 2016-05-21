var url = '/centre/';
var lat = 41.732895;
var lng = 1.793109;
var centres = [];
centres_publics.map(function(centre, i) {
    centre.fields.id = centre.pk;
    centres.push(centre.fields);
});
centres_privats.map(function(centre, i) {
    centre.fields.id = centre.pk;
    centres.push(centre.fields);
});

var map;
var markers = {};
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng },
        zoom: 8,
        scrollwheel: true,
        disableDefaultUI: true,
        draggable: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP, //TERRAIN,SATELLITE,ROADMAP,HYBRID
        styles:[{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#e0efef"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":100},{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"off"},{"lightness":700}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#80cbc4"}]}]
    });
    for( var i = 0; i < centres.length; i++) {
        var marker = new google.maps.Marker({
            position: { lat: parseFloat(centres[i].lat), lng: parseFloat(centres[i].lng)},
            title: centres[i].name,
            map: map,
            title: centres[i].location_name,
            icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png', //centres[i].isPublic ? 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            centre_id: centres[i].id
        });
        markers[centres[i].id] = marker;
        marker.addListener('click', function() {
            window.location.href = url + this.centre_id;
        });
    }
}

$('.centres').on('mouseover', function() {
    var id = $(this).attr('id');
    markers[id].setIcon("http://maps.google.com/mapfiles/ms/icons/yellow-dot.png")
});

$('.centres').on('mouseout', function() {
    var id = $(this).attr('id');
    markers[id].setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png")
});
