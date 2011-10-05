function init_jquery_effects() {
	$('.tag-form').hide();

	$('.add-tag').click(function() {		
		var tag_form = $(this).siblings('.tag-form');
		if (tag_form.is(':visible')) {
			$(this).text('Bæta við merkingu');		
		}
		else {
			$(this).text('Hætta við að bæta við merkingu');
		}
		$(this).siblings('.tag-form').toggle('slow');
	});

	$('.submit-tag').click(function(event) {
		var submit_button = $(this);
		var submit_type = submit_button.attr('class').split(' ')[1];
		$.post('/api/community/'+submit_type+'/tag/', {item:$(this).parent().siblings('h2').text(), tags:$(this).siblings('.input-tags').val()}, function(data) { 
			$.each(data, function() {
				var tags = submit_button.parent().siblings('.tags');
				if (tags.text() == 'Engin merki skráð') {
					tags.text('Merkingar: '+this.tag);
				}
				else {
					tags.text(tags.text() + ', ' + this.tag);
				}
			});
			submit_button.siblings('.input-tags').val('');
			submit_button.parent().siblings('.add-tag').click();
		});
		event.preventDefault();
	});
}

$(init_jquery_effects);
