function make_author_add() {
	$('.author-item').click(function(event) {
		var author_id = $(this).attr('id');
		if ($(this).hasClass('not-selected')) {
			$('#add-author').append('<input type="hidden" name="3-coauthors" id="id-'+author_id+'" value="'+author_id.replace('coauthor_','')+'"/>');
			$(this).removeClass('not-selected');
		}
		else {
			$('#id-'+author_id).remove();
			$(this).addClass('not-selected');
		}
	});
}

$(make_author_add);
