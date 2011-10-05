function init_js() {
    $('.hide-on-load').hide();
    $('.change-form').click(function(event) {
	event.preventDefault();
	$(this).hide();
	$(this).siblings('.input').show(1000);
    });
}

function schools() {
    $('#input_school').bind('keyup change', function() {
	var school_links = $('#school_list li');
	
	// Get search string which is the last value in the input field
	// i.e. split the string at commas (,) and search string is the
	// last string in array (we trim it to ignore leading and
	// trailing whitespace
	var search = $.trim($(this).val());
	
	// If there is a search string slideUp every cloud link that
	// does not include the search word and slideDown all that
	// do include it
	if (search.length > 2) {
	    school_links.filter(':not(:contains("'+search+'"))').hide();
	    school_links.filter(':contains("'+search+'")').show();
	    $('#school_list').show(200);
	}
	else {
	    $('#school_list').hide(200);
	}
    });

    $('#input_school').blur(function() {
	$('#school_list').hide(200);
    });
    

    $('.raindrop').click(function(event) {
	$('#input_school').val($(this).text());
	$('#school_list').hide(200);
    });

    $('#profile_form').submit(function(event) {
	if ($('#input_school').val().length > 0) {
	    school_id = $('#'+$('#input_school').val()).parent().attr('id');
	    $('#input_school').hide();
	    $('#input_school').val(school_id.replace('school_',''));
	}
	else {
	    $('#input_school').remove();
	}
    });

    $('.remove-school').click(function(event) {
	event.preventDefault();
	$(this).parent().remove();
	$('#profile_form').submit();
    });
}


$(init_js);
$(schools);
