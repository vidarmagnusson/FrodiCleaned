/**
 * Function which manages everything related to the abbreviations dialog
 * from opening the dialog to making suggestions clickable.
 *
 * One trigger makes the topics suggestions clickable and fills in the value
 * of a suggestion into the abbreviation input field
 *
 * One trigger manages what happens when a user tries to submit a form (checks
 * whether subjects entered have abbreviations and opens the dialog if any
 * abbreviation is missing. If nothing is missing it lets the user continue to
 * the next step.
 */
function check_professions() {
	// When the form is submitted we either pass it through or open the
	// abbreviation dialog (woah! this is a large an complicated trigger)
	$('#submit-professions').click(function(event) {
	    // If the subjects and topics input fields are not empty
	    // if they are empty we do nothing (return false) which is
	    // done waaay down in the else clause
	    if ($.trim($('#0-profession-input').val()) != '') {
		// Get the path which is an attribute of the submit button
		var path = $(this).attr('path');
		// Set professions as parameters
		var data = { professions:$('#0-profession-input').val()};
		// AJAX call to get the abbreviations (returns a JSON
		// object)
		$.getJSON(path, data, function(data) {
		    
		    // If we get a subject abbreviation...
		    if(data.success) {
			if (data.found_all) {
			    $.each(data.professions_found, function(item) {
				$('#0-profession-wrapper').append('<input type="hidden" name="0-profession" value="'+this.id+'">');
			    });
			}
			else {
			    event.preventDefault();
			}
		    }
		    else {
			event.preventDefault();
		    }
		});
	    }
	    else {
		event.preventDefault();
	    }
	});
}

/**
 * A Lambda function that actually runs all the functions in this .js file
 */
$(function(){
	// This page is largely synchronous
	$.ajaxSetup({async:false});

	// Create the abbreviations dialog
	check_professions();
});

