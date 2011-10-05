/**
 * Function to clear all the important fields
 *
 * Used e.g. when document has been loaded to remove everything which
 * might remain from a previous work with the site
 */
function clear_fields() {
	// Clear the important form fields (hidden)
	$('#id_0-subjects').val('');
	$('#id_0-topics').val('');

	// Clear abbreviations input fields
	$('#subjects-abbreviation').val('');
	$('#topics-abbreviation').val('');

	// Clear input fields
	$('#subjects-input').val('');
	$('#topics-input').val('');
}

/**
 * Function to clear error messages (an classes)
 *
 * Assumes errors are marked with class 'ui-state'error' and error messages
 * are contained within elements who have class 'errorlist'
 */
function clear_errors() {
	// Remove eventual error marks (class 'ui-state-error')
	$('.ui-state-error').removeClass('ui-state-error');
	$('.errorlist').each(function(index) {
	    $(this).text('');
	});
}

/**
 * A function which creates the abbreviations dialog using jquery ui
 * The dialog is contained within a div with id 'abbreviations-form'
 * The abbreviation dialog should have two buttons 'Senda inn' which
 * stands for 'Submit' and 'Hætta við' which stands for 'Cancel' (it
 * also has the close button in the top right corner).
 *
 * Assumes the abbreviations dialog has id 'abbreviations-form' and
 * that it contains a form with id 'subjects_and_topics_form'
 */
function create_abbreviations_dialog() {
    $('#abbreviations-form').dialog({
	autoOpen: false,
	height: 420,
	width: 460,
	modal: true,
	buttons: {
	    "Senda inn": function() {
		// Submit button pressed

		// Get subject and topic abbreviations
		var subject_abbreviation = $('#subjects-abbreviation').val();
		var topic_abbreviation = $('#topics-abbreviation').val();

		// Clear eventual errors from previous tries
		clear_errors();

		// Get the post form within the abbreviations dialog
		var post_form = $('#subjects_and_topics_form');

		// Submit the form using post (returns a JSON object)
		$.post(post_form.attr('action'), post_form.serialize(), function(data) {
			// If successful...
			if(data.success) {
				// Fill the hidden subjects and topics fields
				// with the returned id for subjects and topics
				// respective (abbreviations have already been
				// created for these ids.
				$('#id_0-subjects').val(data.subject_id);
				$('#id_0-topics').val(data.topic_id);

				// After subjects and topics have been set
				// Submit the main form and continue to the
				// next step
				$('form:first').submit();

				// Then close this dialog
				$(this).dialog('close');
			}
			// If not successful
			else {
				// Add error class 'ui-state-error' to the originator
				$('#'+data.origin+'-abbreviation').addClass('ui-state-error');
				// Set the error text with the reason of failure
				$('#'+data.origin+'-abbreviation-error').text(data.reason);
			}
		});
	    },
	    "Hætta við": function() {
		// Cancel pressed

		// Clear the abbreviations fields
		$('#subjects-abbreviation').val('');
		$('#topics-abbreviation').val('');

		// Clear any eventual error texts
		clear_errors();

		$(this).dialog( "close" );
	    }
	},
	close: function() {
		$('#subjects-abbreviation').val('');
		$('#topics-abbreviation').val('');

		// Clear errors
		clear_errors();
	}
    });
}
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

