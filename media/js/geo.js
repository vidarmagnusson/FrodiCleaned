function update_location(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var data = {format:'json', addressdetails:1, lat:latitude, lon:longitude};
    var path = 'http://nominatim.openstreetmap.org/reverse';
    $.getJSON(path, data, function(data) {
	if (data.address) {
	    var address_data = {postcode:data.address.postcode};
	    var address_path = 'http://mrn.pagekite.me/api/samfelag/location/';
	    $.getJSON(address_path, address_data, function(location) {
		if (location.success) {
		    if ($('#location').length) {
			$('#location').html(location.municipality);
		    }
		}
	    });
	}
    });
}

function get_location() {
    if (Modernizr.geolocation) {
	navigator.geolocation.getCurrentPosition(update_location);
    } else {
	alert("FAIL");
    }
}

$.ajaxSetup({async:false});
$(get_location);
