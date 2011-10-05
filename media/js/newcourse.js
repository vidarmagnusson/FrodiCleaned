function init_jquery_effects() {
	// Only show one box which asks for the name
        $('#div-course-information').hide();

	// Hide description texts
	$('.description-text').hide();

	// Hide everything related to the abbreviation (subjects,topics,course)
        $('#div-abbreviation').hide();
        $('#div-subjects-abbreviation').hide();
        $('#div-topics-abbreviation').hide();

	// Hide evaluation input
        $('#div-evaluation').hide();

	// Reset form
        $('form')[0].reset();
	$('input, textarea').keypress(function(event){
		if(event.keyCode == '13') {
		    event.preventDefault();
		}
	    });

	// Put focus on search/create box
        $('#subjects').focus();
	$('#subjects').siblings('.description-text').show('slow');
	$('#topics').siblings('.description-text').show('slow');
}


/* Check whether *descriptive name* has some value */
function check_basic_info() { 
    return ($('#subjects').val() != '') &&
	($('#subjects-abbreviation').val() != '') &&
	($('#topics').val() != '') &&
	($('#topics-abbreviation').val() != '') &&
	($('#level').val() != '') &&
	($('#credits').val() != '');
}

function check_all() {
    return ($('#descriptive-name').val() != '') &&
	($('#subjects').val() != '') &&
	($('#subjects-abbreviation').val() != '') &&
	($('#topics').val() != '') &&
	($('#topics-abbreviation').val() != '') &&
	($('#level').val() != '') &&
	($('#credits').val() != '') &&
	($('#prerequisites').val() != '') &&
	($('#description').val() != '') &&
	($('#knowledge-goals').val() != '') &&
	($('#skill-goals').val() != '')	&&
	($('#competence-goals').val() != '') &&
	($('#evaluation').val() != '');
}

/* Pad a variable (padvar) up to a given length with
   a supplied pad */
function pad( padvar, pad_length, pad ) {
	var padded = ''+padvar;
	while (padded.length < pad_length) {
		padded = pad + padded;
	}
	return padded;
}

function publish_side_information(element) {
    var id = element.attr('id');
    var label = element.siblings('label').text();

    $('#item-'+id).siblings('.information-label').html(label+' <img width="10" src="/media/myndir/pencil.png">');		
    $('#item-'+id).text(element.val());	
    element.parent().hide('slow');

    return true;
}



function input_change() {
    $('input').change(function() {
	    
	});
}

function show_course_abbreviation() {
    if (check_basic_info()) {
	var subject = $('#subjects-abbreviation').val().toUpperCase();
	var topic = $('#topics-abbreviation').val().toUpperCase();
	var level = $('#level').val();
	var credits = pad($('#credits').val(), 2, '0');
	
	$('#id-abbreviation').html(subject+level+topic+credits);
	$('#div-abbreviation').fadeIn(4000);
    }
}

function input_blur() {
    $('.normal-input, select').blur(function() {
	    //$(this).siblings('.description-text').hide('fast');
	    if ($(this).val() != '') { 
		publish_side_information($(this));
		$(this).parent().hide(2000); 
		show_course_abbreviation();
	    }
    });
    
    $('#credits-slider').blur(function() {
	    //$(this).siblings('.description-text').hide('fast');
	    if ($('#credits').val() != '') { 
		publish_side_information($('#credits'));
		$(this).parent().hide(2000); 
		show_course_abbreviation();
	    }
	    });

    $('select').click(function() {
	    //$(this).siblings('.description-text').hide('fast');
	    if ($(this).val() != '') { 
		publish_side_information($(this));
		$(this).parent().hide('fast'); 
		show_course_abbreviation();
	    }
	    });

    $('#subjects-abbreviation').blur(function (){
	    if ($(this).val() != '') {
		if ($(this).val().length == 4) {
		    $(this).css('background: #ffffff');
		    publish_side_information($(this));
		    $(this).parent().hide('fast');
		}
		else {
		    $(this).css('background: #ff0000');
		    alert("Skammstöfun námsgreina verður að vera 4 stafir");
		}
	    }
	});

    $('#topics-abbreviation').blur(function (){
	    if ($(this).val() != '') {
		if ($(this).val().length == 2) {
		    publish_side_information($(this));
		    $(this).parent().hide('fast');
		}
		else {
		    alert("Skammstöfun viðfangsefna verður að vera 2 stafir");
		}
	    }
	    });
}

function input_focus() {
    $('input, textarea, a, select').focus(function() {
	    $(this).siblings('.description-text').show('fast');
	    /*if ($(this).attr('id') != 'subjects' &&
		$(this).attr('id') != 'topics') {
		if ($('#subjects').val() != '') {
		    publish_side_information($('#subjects'));
		    $('#subjects').parent().hide('slow');
		    if( $('#subjects-abbreviation').val() == '') {
			get_abbreviation_json('subjects');
		    }
		}
		if ($('#topics').val() != '') {
		    publish_side_information($('#topics'));
		    $('#topics').parent().hide('slow');
		    if( $('#topics-abbreviation').val() == '') {
			get_abbreviation_json('topics');
		    }
		}
		}*/
	});
}

function make_editable() {
    $('.edit').click(function() {
	var name = $(this).attr('id').substring(5); //remove preceding 'list-'
	$('#div-'+name).show('slow');
	$('#'+name).focus();
	});
}

function make_credit_slider() {
    $('#credits').hide();
    $('#div-credits-value').removeClass('hidden');

    $('#credits-slider').slider({
	    min: 0, max: 15, step: 1,
	    slide: function( event, ui ) {
		$('#credits').val( ui.value );
		$('#credits-value').text( ui.value );
		$('#credits-slider').focus();
	    }
	});
}

RegExp.escape = function(str) {
	var specials = new RegExp("[.*+?|()\\[\\]{}\\\\]", "g"); // .*+?|()[]{}\
	return str.replace(specials, "\\$&");
}

function remove_item(list_element){
	var name = list_element.attr('class').substring(5);
	var remove_text = list_element.text();
	remove_text = remove_text.substring(0,(remove_text.length-1));

	var re = new RegExp("^\\* "+RegExp.escape(remove_text)+"\n", 'm');
	$('#'+name).val($('#'+name).val().replace(re,''));

	list_element.remove();
}

function add_to_bulletlist(event, element) {
	if (event.keyCode == '13') {
		event.preventDefault();

		var value = element.val();
		if( value != '' ) {
			var name = element.attr('id').substring(6);
			var re = new RegExp("^\\* "+RegExp.escape(value)+"\n", 'm');
			if (!$('#'+name).val().match(re,'')) {
			    element.parent().before('<li class="item-'+name+'">' + value + '<span class="bullet_delete" onclick="remove_item($(this).parent())">X</span></li>');
			    $('#'+name).val($('#'+name).val()+'* '+value+'\n');
			    element.val('');
			}
		}
	}
}

function add_evaluation_goal(event, element) {
    if (event.keyCode == '13') {
	event.preventDefault();
	var value = element.val();
	element.parent().before('<li>' + value + '<span class="bullet_delete" onclick="$(this).parent().remove();">X </span></li>');
	
	$('#inputlist-evaluation').append('<li style="list-style: none"><strong>Hvernig verður <em>'+value+'</em> metið?</strong><ul><li><input class="goal-item" onKeypress="add_to_bulletlist(event, $(this));" id="input-evaluation"/></li></ul></li>');
	
	var name = element.attr('id').substring(6);
	$('#'+name).val($('#'+name).val()+'* '+value+'\n');
	element.val('');
    }
}

function show_goaldescription(element) {
    element.parent().siblings('.description-text').show('slow');
}

function hide_goaldescription(element) {
    element.parent().siblings('.description-text').hide('slow');
}

function make_bulletlist() {
    $('#knowledge-goals').hide();
    $('#skill-goals').hide();
    $('#competence-goals').hide();
    $('#evaluation').hide();
    $('.goal-input').removeClass('hidden');
    $('.evaluation-goal-input').removeClass('hidden');
    $('.bulletheading').removeClass('hidden');

    $('.goal-item, .evaluation-goal-item').focus(function() {
	    show_goaldescription($(this).parent());
	});

    $('.goal-item').keypress(function(event) { 
	    add_to_bulletlist(event, $(this));
	});
    
    $('.evaluation-goal-item').keypress(function(event) { 
	    add_evaluation_goal(event, $(this));
	    $('#evaluation').siblings('.description-text').show();
	    $('#div-evaluation').show('slow');
	});
}

function set_autocompletion(id) {
    $('#'+id).autocomplete( {
	    source: '/api/namskra/framhaldsskolar/'+id+'/autocomplete',
		minLength: 2,
		select: function( event, ui ) {
		$(this).focus();
		event.preventDefault();
		var uptonow = $(this).val();
		var parts = uptonow.split(',');
		parts[parts.length-1] = ui.item.value;
		$(this).val(parts.join(', '));
	    }
	});   
}

function make_autocompletion() {
    set_autocompletion('subjects');
    set_autocompletion('topics');
}

function get_abbreviation_json(entity) {
    var path = '/api/namskra/framhaldsskolar/'+entity+'/'+$('#'+entity).val();
    $.getJSON(path, function(data) {
	    var entity_abbr = entity + '-abbreviation';
	    if (data.abbr) { 
		$('#'+entity_abbr).val(data.abbr);
		publish_side_information($('#'+entity_abbr));
	    }
	    else { 
		$('#'+entity_abbr).siblings('label').html('Skammstöfun fyrir '+$('#'+entity).val());
		$('#div-'+entity_abbr).show('fast'); 
	    }
	});
}

function show_course_information() {
    $('#create-course').click(function() {
	    if (($('#subjects').val() != '') && ($('#topics').val() != '')) {
		$(this).hide();
		$('#div-course-information').slideDown(5000);
		
		publish_side_information($('#subjects'));
		get_abbreviation_json('subjects');		
		$('#subjects').siblings('.move-to-course').removeClass('hidden');
		publish_side_information($('#topics'));
		get_abbreviation_json('topics');
		$('#topics').siblings('.move-to-course').removeClass('hidden');
	    }
    	});
}

function make_transfer() {
    $('.move-to-course').click(function() {
	    if ($('#descriptive-name').val() != '') {
		publish_side_information($('#descriptive-name'));
		}
	    if ($('#subjects').val() != '') {
		publish_side_information($('#subjects'));
	    }
	    if ($('#topics').val() != '') {
		publish_side_information($('#topics'));
	    }
	    if ($('#subjects-abbreviation').val() != '') {
		publish_side_information($('#subjects-abbreviation'));
	    }
	    if ($('#topics-abbreviation').val() != '') {
		publish_side_information($('#topics-abbreviation'));
	    }
	    if ($('#level').val() != '') {
		publish_side_information($('#level'));
	    }
	    if ($('#credits').val() != '') {
		publish_side_information($('#credits'));
	    }
	    if ($('#prerequisites').val() != '') {
		publish_side_information($('#prerequsites'));
	    }
	    if ($('#description').val() != '') {
		publish_side_information($('#description'));
	    }
	    if ($('#knowledge-goals').val() != '') {
		publish_side_information($('#knowledge-goals'));
	    }
	    if ($('#skill-goals').val() != '') {
		publish_side_information($('#skill-goals'));
	    }
	    if ($('#competence-goals').val() != '') {
		publish_side_information($('#competence-goals'));
	    }
	    if ($('#evaluation').val() != '') {
		publish_side_information($('#evaluation'));
	    }

	    show_course_abbreviation();
		/*      	    var value = $(this).siblings('textarea').val();
	    var label = $(this).siblings('label').text();
	    var id = $(this).siblings('ul').attr('id').substring(10);
	    if (value != '') {
		$('#item-'+id).siblings('.information-label').html(label+' <img width="10" src="/media/myndir/pencil.png">');
                $('#item-'+id).append('<ul>'+value.replace(/\n/gm,'<br/>')+'</ul>');
                $(this).parent().hide('slow');
		}*/
	    
	    if( check_all() ) {
		$('#submit').removeClass('hidden');
	    } 
	});
}


$(init_jquery_effects);
$(show_course_information);

$(input_change);
$(input_blur);
$(input_focus);

$(make_editable);
$(make_credit_slider);
$(make_bulletlist);
$(make_autocompletion);
$(make_transfer);
