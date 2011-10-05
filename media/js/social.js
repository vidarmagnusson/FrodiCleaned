function init_js() {
    $('.hide-on-load').hide();
}

function enable_tagging() {
    $('.tag-form').hide();
    $('.cancel-tag').hide();

    $('.add-tag').click(function(event) {
	event.preventDefault();
	$(this).hide();
	$(this).siblings('.tag-form').show(1000);
	$(this).siblings('.cancel-tag').show();
    });

    $('.cancel-tag').click(function(event) {
	event.preventDefault();
	$(this).hide();
	$(this).siblings('.tag-form').hide(1000);
	$(this).siblings('.add-tag').show();
    });

    $('.tag-form').submit( function(event) {
	event.preventDefault()
	var post_form = $(this);
	$.post(post_form.attr('action'), post_form.serialize(), 
	       function(data) {
		   if (data.success) {
		       $.each(data.tags, function(item) {
			   post_form.siblings('.tag-list').append(' <a href="/samfelag/flokkar/'+this.slug+'">'+this.tag+'</a>');
			   post_form.children('.tag_form_tag').val('');
		       });
		   }
	       });
    });
}

function enable_commenting() {
    $('.add-comment').click(function(event) {
	event.preventDefault();
	$(this).hide();
	$(this).parent().siblings('.comment-form').show(1000);
    });

    $('.comment-form').submit( function(event) {
	event.preventDefault()
	var post_form = $(this);
	$.post(post_form.attr('action'), post_form.serialize(), 
	       function(data) {
		   if (data.success) {
		       post_form.siblings('.comment-list').append('<div class="comment"><img src="'+data.user_avatar+'" title="'+data.user_name+'" width="30"><div class="comment-author"><a href="'+data.user_link+'" title="'+data.user_name+'">'+data.user_name+'</a></div>'+data.comment+'<div class="comment-time">'+data.published+'</div></div>');

		       post_form.children('.comment_form_comment').val('');
		   }
	       });
    });
}

$(init_js);
$(enable_tagging);
$(enable_commenting);
