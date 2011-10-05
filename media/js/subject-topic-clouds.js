/**
 * Function which manages all input field initiated triggers.
 *
 * One trigger shows the subjects cloud and hides the topics cloud whenever
 * the subjects input gets focus
 *
 * One trigger is used to filter the clouds whenever the user starts typing 
 * in the input fields (who have the 'input-filter' class set).
 * On every keystroke the cloud either hides or shows links containing (or not)
 * the current value of the input field in the respective cloud
 *
 * One trigger is used to populate the topics cloud when the topics input gets
 * focus and the user has put subjects in the subjects input. This trigger uses
 * AJAX to get a JSON object through a web service and fills in accordingly.
 * If the user has not put anything in the subjects nothing happens and the
 * subjects cloud is still visible, if the trigger populates the topics cloud
 * it then hides the subjects cloud and shows the topics cloud
 *
 * Assumes that input field and cloud id's are written in the exact same way
 * except that instead of input (for input field) it says cloud, e.g. the
 * input and cloud id's for subjects would be subjects-input and subjects-cloud
 */
function input_to_clouds() {
	// Show subjects cloud whenever subjects input field gets focus
	$('#subjects-input').focus(function() {
		// subject and topic lists are wrappers around each cloud
		$('#subject-list').show();
		$('#topic-list').hide();
	});

	// Detect when a new character is added (or removed)
	$('.input-filter').bind('keyup change', function() {
		// From input field name get cloud name
		var cloud = $(this).attr('id').replace('input','cloud');
		// Find all links within the cloud
		var cloud_links = $('#'+cloud+' a');

		// Get search string which is the last value in the input field
		// i.e. split the string at commas (,) and search string is the
		// last string in array (we trim it to ignore leading and
		// trailing whitespace
		var search = $.trim($(this).val().split(',').pop())

		// If there is a search string slideUp every cloud link that
		// does not include the search word and slideDown all that
		// do include it
		if (search) {
			cloud_links.filter(':not(:contains("'+search+'"))').slideUp();
			cloud_links.filter(':contains("'+search+'")').slideDown();
		}
		// If there is no search string (empty input field) show all links
		else {
			cloud_links.slideDown();
		}
	});

	// Populate topics cloud when topics-input gets focus
	$('#topics-input').focus(function() {
		// We only populate the cloud if subjects input has any value
		if ($('#subjects-input').val() != '') {

			// Grab the path from a path attribute of topics input
			var path = $(this).attr('path');
			// Set data 'subjects' with the value of subjects input
			var data = { subjects:$("#subjects-input").val() };

			// GET data using AJAX
			$.getJSON(path, data, function(data) {
				// Find the topics cloud
				var topic_cloud = $('#topics-cloud');

				// If successful create topics cloud
				if (data.success) {
					// Clear the cloud
					topic_cloud.empty();
					// For each item in the list 'cloud'...
					$.each(data.cloud, function(item) {
						// Append it to the topics cloud as a raindrop
						topic_cloud.append('<a id="'+this.element+'" class="raindrop '+this.size+'" href="#">'+this.element+'</a> ');
					});
				}
				// If not successful
				else {
					// Set the cloud text as the message
					topic_cloud.html(data.message);
				}
			});

			// Hide the subjects cloud and show the topics cloud
			// Notice that this is within the "if subjects input != ''
			$('#subject-list').hide();
			$('#topic-list').show();
		}
	});
}

/**
 * Function which manages all triggers initiated by the clouds.
 *
 * One trigger acts on all cloud links which have the class 'raindrop' (yes,
 * it is a rather bad analogy that the clouds have raindrops which can land
 * in input fields but this is our code and we can use tacky analogies).
 * When a raindrop is clicked the trigger adds it to the last position of the
 * input field value, i.e. substitutes the last subject (after the last comma)
 * with the value. Does also make the list prettier by adding a space behind
 * each comma (ooohh, now that _is_ readable)
 *
 * Assumes that input field and cloud id's are written in the exact same way
 * except that instead of input (for input field) it says cloud, e.g. the
 * input and cloud id's for subjects would be subjects-input and subjects-cloud
 */
function clouds_to_input() {
	// When a raindrop (link in a cloud) is clicked)
	// add it to the respective input field
	$('.raindrop').live('click', function(event){
		event.preventDefault();

		// Get the input field id for this cloud
		var input = $('#'+$(this).parent().attr('id').replace('cloud','input'));
		// Get the value (the text bit of the raindrop link)
		var value = $(this).text();

		// If we cannot find the raindrop in the input field we add it
		if (input.val().search(value) < 0) {
			// Start by splitting the input field value (by comma)
			var split_input = input.val().split(',');

			// Trim each item in the list
			$.each(split_input, function(item) { split_input[item] = $.trim(this); });

			// Substitute the last entry with the value
			// This works well with the filter which can then
			// be used to complete a word being typed in
			// This also adds a trailing comma to prepare for
			// another word (or at least not substitute the one
			// that just got selected
			split_input[split_input.length-1] = value + ', ';

			// The words are then joined together and put in the
			// input field (which then gets focus)
			input.val(split_input.join(', '));
			input.focus();
		}
	});
}

/**
 * A Lambda function that actually runs all the functions in this .js file
 */
$(function(){
	// Initiate input to cloud triggers
	input_to_clouds();

	// Initiate cloud to input triggers
	clouds_to_input();

	// Put focus on subject input
	$('#subjects-input').focus();
});
