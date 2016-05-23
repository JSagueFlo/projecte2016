var map;
var markers = [];
var info_windows = [];

// Inicialització del mapa que mostra la localització d'un centre i totes les seves boies
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng},
        zoom: 15,
        scrollwheel: false,
        disableDefaultUI: true,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP, //TERRAIN,SATELLITE,ROADMAP,HYBRID
        styles: [{
            "featureType": "landscape.natural",
            "elementType": "geometry.fill",
            "stylers": [{"visibility": "on"}, {"color": "#e0efef"}]
        }, {"featureType": "poi", "stylers": [{"visibility": "off"}]}, {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [{"lightness": 100}, {"visibility": "simplified"}]
        }, {
            "featureType": "road",
            "elementType": "labels",
            "stylers": [{"visibility": "off"}]
        }, {
            "featureType": "transit.line",
            "elementType": "geometry",
            "stylers": [{"visibility": "on"}, {"lightness": 700}]
        }, {"featureType": "water", "elementType": "all", "stylers": [{"color": "#80cbc4"}]}]
    });

    //centre
    var marker_centre = new google.maps.Marker({
        position: { lat: centre_lat, lng: centre_lng},
        map: map,
        title: centre_name,
        icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });
    var info_window_centre ;
    marker_centre.addListener('mouseover', function() {
        if (!this.isDisplayed) {
            info_window_centre = new google.maps.InfoWindow({
                content: '<div class="info-window">'+ this.title +'</div>'
            });
            info_window_centre.open(map,this);
            this.isDisplayed = true;
        }
        console.log(this.isDisplayed);

    });
    marker_centre.addListener('mouseout', function() {
        info_window_centre.close();
        this.isDisplayed = false;
    });

    //boies
    for( var i = 0; i < boies.length; i++) {
        markers.push(
            new google.maps.Marker({
                position: { lat: parseFloat(boies[i].lat), lng: parseFloat(boies[i].lng)},
                map: map,
                title: boies[i].location_name,
                icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                boia_id: data[i].pk,
                isDisplayed: false,
                i: i
            })
        );
        markers[i].addListener('click', function() {
            window.location.href = url + this.boia_id;
        });
        markers[i].addListener('mouseover', function() {
            if (!this.isDisplayed) {
                info_windows.push(
                    new google.maps.InfoWindow({
                        content: '<div class="info-window">'+ this.title +'</div>'
                    })
                );
                info_windows[this.i].open(map,this);
                this.isDisplayed = true;
            }
            console.log(this.isDisplayed);

        });
        markers[i].addListener('mouseout', function() {
            info_windows[this.i].close();
            this.isDisplayed = false;
        });
    }
}
