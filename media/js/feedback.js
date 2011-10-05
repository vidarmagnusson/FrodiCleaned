function init_jquery_effects() {
	$('.comment_form').hide();

	$('.add-comment').click(function() {		
		$(this).siblings('.comment_form').slideToggle('slow');
	});
}

$(init_jquery_effects);
$(scroll_around);

