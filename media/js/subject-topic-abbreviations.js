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
function manage_abbreviations_dialog() {

	// Make suggestions clickable and if clicked their id and their parents
	// id are used to fill in the correct values
	$('.suggestion').live('click', function(event) {
		// The abbreviation itself is contained in the parent's id
		$('#topics-abbreviation').val($(this).parent().attr('id'));

		// The string value is contained in this elements id
		// The input field value is substituted for the suggestion
		$('#topics-input').val($(this).attr('id'));
	});

	// When the form is submitted we either pass it through or open the
	// abbreviation dialog (woah! this is a large an complicated trigger)
	$("#submit-subjects-topics").click(function(event) {
		// Hide suggestions within the dialog (we don't know if
		// there are going to be any suggestions) and empty the
		// suggestions list
		$('#suggestions').hide();
		$('#topics-suggestions').empty();

		// If the subjects and topics input fields are not empty
		// if they are empty we do nothing (return false) which is
		// done waaay down in the else clause
		if (($.trim($('#subjects-input').val()) != '') && ($.trim($('#topics-input').val()) != '')) {
			// Get the path which is an attribute of the submit button
			var path = $(this).attr('path');
			// Set subjects and topics as parameters
			var data = { subjects:$("#subjects-input").val(),
				     topics:$("#topics-input").val() };

			// AJAX call to get the abbreviations (returns a JSON
			// object)
			$.getJSON(path, data, function(data) {

				// If we get a subject abbreviation...
				if(data.subject_abbreviation) {
					// Hide the input field asking for an abbreviation
					$('#subjects-abbreviation').hide();
					// Hide the description (since we're not asking the user to do anything)
					$('#subjects-abbreviation-description').hide();

					// The subject id which we have also received is put into the hidden input field
					$('#id_0-subjects').val(data.subject_id);

					// Inform the user about the abbreviation
					$('#subjects-abbreviation-text').html('<strong>'+data.subject_abbreviation+'</strong>');
					// Put the abbreviation is the field (which we have hidden)
					$('#subjects-abbreviation').val(data.subject_abbreviation);
				}
				// If we didn't get a subject abbreviation...
				else {
					// Remove any value from the main input field
					$('#id_0-subjects').val('');

					// Remove value from abbreviation input field
					$('#subjects-abbreviation').val('');

					// Show the abbreviation input field and its corresponding description text
					$('#subjects-abbreviation').show();
					$('#subjects-abbreviation-description').show();

					// Get known subjects (those found in the system) and join in a comma separated string
					var found = data.subjects_found.join(', ');
					// ... and unknown (not found) - do the same except we add emphasis and mark as unknown (þekkist ekki)
					var not_found = data.subjects_not_found.join('</em>, <em>');
					if (not_found) { not_found = '<em>'+not_found+' (þekkist ekki)</em>'; }
					// Separator between known and unknown
					var separator = ' - ';
					if((found == '') || (not_found == '')) { separator = ''; }
					// Add found, separator and not found to the abbreviation text
					$('#subjects-abbreviation-text').html(found+separator+not_found);
				}

				// If we get a topic abbreviation we've found everything...
				if(data.topic_abbreviation) {
					// ... therefore it is enough to just add the topic id to the hidden main topics input field
					$('#id_0-topics').val(data.topic_id);
				}
				// If we did not get a topic abbreviation...
				else {
					// Clear the main topics input field
					$('#id_0-topics').val('');

					// Clear the topics abbreviation input field
					$('#topics-abbreviation').val('');

					// Show the input field and its corresponding description box
					$('#topics-abbreviation').show();
					$('#topics-abbreviation-description').show();

					// Join known (found) topics together and mark them as known (þekkt)
					var found = data.topics_found.join('(þekkt), ');
					if (found) { found = found +' (þekkt)'; }

					// Do the same to unknown (not found) topics but mark them as not used before (ekki notað áður)
					var not_found = data.topics_not_found.join('</em> (ekki notað áður), <em>');
					if (not_found) { not_found = '<em>'+not_found+' (ekki notað áður)</em>'; }
		    
					// Spearator (either nothing or ' - '
					var separator = ' - ';
					if((found == '') || (not_found == '')) { separator = ''; }

					// Add found, separator, and not found to abbreviation text
					$('#topics-abbreviation-text').html(found+separator+not_found);

					// If we have any topic suggestions
					if (data.topic_suggestions.length) {
						// Show the suggestions bux
						$('#suggestions').show();
						// Get the suggestions list
						var suggestion_list = $('#topics-suggestions');
						// For each suggestion we append it to the list
						$.each(data.topic_suggestions, function(item) { suggestion_list.append('<li id="'+this.abbreviation+'"><a href="#" id="'+this.topics+'" class="suggestion">'+this.abbreviation+' - '+this.topics+'</a></li>'); });
					}
				}
			});

			// If the main (hidden) subjects and topics fields are empty...
			if (($('#id_0-subjects').val() == '') || ($('#id_0-topics').val() == '')) {
				// We add the input subjects and topics to a hidden field in the abbreviation dialog form (used to post abbreviations)
				$('#subjects-list').val($('#subjects-input').val());
				$('#topics-list').val($('#topics-input').val());

				// Open the abbrevations dialog
				$('#abbreviations-form').dialog('open');

				// Prevent the form from being submitted
				event.preventDefault();
			}
		}
		else {
			// Remember this else... it's the else triggered if 
			// either subjects or topics are empty
			// and then we prevent the form from being submitted
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

	// Clear all fields
	clear_fields();
	
	// Create the abbreviations dialog
	create_abbreviations_dialog();
	// Manage the abbreviations dialog
	manage_abbreviations_dialog();
});

