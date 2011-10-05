function init_js() {
    $('.hide-on-load').hide();
    $('#show-extra-information').click(function(event) {
	event.preventDefault();
	$('#extra-information-input').toggle(500);
    });

}

function make_article() {
		$(this).animate({height:400}, 1000);    
}

function resize_textbox(textbox) {
    var max_height=400;
    var min_height=40;
    var box_height=textbox.height();
    var grow_by = 30;

    textbox.val().length
}


function manage_submit() {
    $('#community-form').submit(function(event) {
	if ($('#id_community_note').length && $('#id_community_note').val() == document.getElementById('id_community_note').defaultValue) {
	    $('#id_community_note').val('');
	}
	if ($('#id_community_title').length && $('#id_community_title').val() == document.getElementById('id_community_title').defaultValue) {
	    $('#id_community_title').val('');
	    alert($('#id_community_title').val());
	}
	if ($('#id_community_tags').length && $('#id_community_tags').val() == document.getElementById('id_community_tags').defaultValue) {
	    $('#id_community_tags').val('');
	}
    });

    $('#id_community_note').bind('keyup change', function() {
	var remaining = 140-$(this).val().length;
	$('#character-counter').text(remaining);
	if (remaining < 0) {
	    $('#character-counter').addClass('red-text');
	}
	else {
	    $('#character-counter').removeClass('red-text');
	}
    });

    $('#id_community_note').bind('paste', function(e) {
	var el = $(this);
        setTimeout(function() {
            var text = $(el).val();
	    if( text.match('^(http|https)://(\\w+\\.){1,}\\w+(:\\d+)*/\\S*\\s*$')) {
		$('.bookmark').show(500);
	    }
        }, 100);
    });

    $('#icon-article').click(function(event) {
	$('#character-counter').hide();
	var note_input = $('#id_community_note');
	var saved_value = note_input.val();
	if (saved_value == document.getElementById('id_community_note').defaultValue) {
	    saved_value = ''
	}
	note_input.replaceWith('<input name="title" class="never-selected-input" id="id_community_title" maxlength="256" value="Titill">');

	if (saved_value) {
	    $('#id_community_title').removeClass('never-selected-input').addClass('not-selected-input');
	    $('#id_community_title').val(saved_value);
	}

	$('#id_community_content').css({height:500});
	$('.article').show(2000);
	$('.left-icon').fadeOut(1000);
    });

    $('#icon-attachment').click(function(event) {
	$('#character-counter').hide();
	$('#id_community_note').replaceWith('<input name="title" class="never-selected-input" id="id_community_title" maxlength="256" value="Titill">');
	$('.file').show(500);
	$('.right-icon').fadeOut(500);
	$('#loading-area').fadeIn(500);
    });

    $('.not-selected-input, .never-selected-input').live('focus', function() {
	$(this).removeClass('not-selected-input').removeClass('never-selected-input').addClass('selected-input');
	if ($(this).val() == this.defaultValue) {
	    $(this).val('');
	}
    });

    $('.selected-input').live('blur', function() {
    	$(this).removeClass("selected-input");
        if ($.trim($(this).val()) == ''){
	    if(this.defaultValue) {
		$(this).val(this.defaultValue);
	    }
	    else {
		$(this).val('');
	    }
	    $(this).addClass('never-selected-input')
    	}
	else {
	    $(this).addClass('not-selected-input');
	}
    });

    $('.tag-suggestion').click(function(event) {
	event.preventDefault();
	var tag = $(this).text();
	var tag_input = $('#id_community_tags');
	
	if (tag_input.hasClass('never-selected-input')) {
	    tag_input.removeClass('never-selected-input').addClass('not-selected-input');
	    tag_input.val(tag);
	}
	else {
	    if (tag_input.val().search(tag) < 0) {
		var tag_input_value = $.trim(tag_input.val());
		if (!tag_input_value.match(',$')) {
		    tag = ', '+tag;
		}
		else {
		    tag = ' '+tag;
		}
		tag_input.val(tag_input_value+tag);
	    }
	}

	tag_input.focus();
    });

    $('.fold-out').click(function(event) {
	event.preventDefault();
	$(this).siblings('.fold-out-input').show('fast');
	$(this).hide();
    });

    $('#id_community_license').bind('change', function() {
	$('#chosen-cc').text($('#id_community_license :selected').text());
	$('#chosen-cc').siblings('.fold-out').show();
	$('#chosen-cc').siblings('.fold-out-input').hide('fast');
    });

    $('.fold-out-close').click(function(event) {
	event.preventDefault();
	$(this).parent().hide('fast');
	$(this).parent().siblings('.fold-out').show();
    });

    $('#change_author').click(function(event) {
	event.preventDefault();
	if ($.trim($('#id_author_input').val()) != '') {
	    $('#original-author-name').text($('#id_author_input').val());
	}
	    $('#original-author-name').siblings('.fold-out').show();
	    $('#original-author-name').siblings('.fold-out-input').hide('fast');
    });

    setup_wmd({
        input: "id_community_content",
        button_bar: "wmd-button-bar",
        preview: "content_preview"
    });
}

$(init_js);
$(manage_submit);
