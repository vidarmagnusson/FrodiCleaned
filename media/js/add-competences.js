function make_dialogs() {
    $('.delete-competence').live('click', function(event) {
	var list_element = $(this).parent();
	var competence_id = (list_element.attr('class')).replace('competence_','');
	$('#competence_text').html(list_element.text());
	$('#competence_to_delete').val(competence_id);
	$('#confirm-delete-dialog').dialog('open');
    });

    $('#confirm-delete-dialog').dialog({
	autoOpen: false,
	height:250,
	modal: true,
	buttons: {
	    "Eyða viðmiði": function() {
		var post_form = $('#delete-competence_form');
		$.post(post_form.attr('action'), post_form.serialize(), function(data) {
		    if (data.success) {
			var remove_class = '.competence_'+$('#competence_to_delete').val();
			$(remove_class).remove();
		    }
		});
		
		$( this ).dialog( "close" );
	    },
	    "Hætta við": function() {
		$( this ).dialog( "close" );
	    }
	}
    });
  
    $('#competence_add-form').dialog({
	autoOpen: false,
	height: 400,
	width: 460,
	modal: true,
	buttons: {
	    "Senda inn": function() {
		var status = false;
		var this_id = $(this).attr('id').replace('_add-form','');
		if ($('#competence_goal').val() == '') { return false; }
		var post_form = $('#competence_form');
		$.post(post_form.attr('action'), post_form.serialize(), 
		       function(data) {
			   if (data.success) {
			       var competence = $('#competence_goal').val() +' <img class="delete-competence" src="/media/icons/eyda.png" alt="Eyða lykilhæfniþætti">';
			       var competence_id = $('#key_competence_choice').val();
			       $('#competence-add-wrapper').append('<input type="hidden" value="'+data.goal_id+'" name="3-key_competence_goals" id="id_key_competence_goal_'+data.goal_id+'" class="competence_'+data.goal_id+'" />');

			       $('#'+competence_id+'_added').append('<li id="item_competence_goal_'+data.goal_id+'" class="competence_'+data.goal_id+'">'+competence+'</li>');
			       $('#competence_goal').val('');
			       $('#key_competence_choice').val('');
			       
			       status = true;
			   }
		       });
		
		if (status) {
		    $(this).dialog( "close" );
		}
	    },
	    "Hætta við": function() {
		$(this).dialog( "close" );
	    }
	}
    });
        
    $(".add-to-list").click(function(event) {
	var competence_id = $(this).attr('id').replace('_add','');
	$('#key_competence_choice').val(competence_id);
	$('#competence_add-form').dialog('open');
	event.preventDefault();
    });

    $('#key_competence_form').submit(function(event) {
	$('.competence_description').each(function (index) {
	    // Grab the path from a path
	    var path = $('#key_competence_submit').attr('path');
	    // Set data 'subjects' with the value of subjects input
	    var data = {choice: $(this).attr('id').replace('_competence',''),
			description: $(this).val()};

	    // GET data using AJAX
	    $.getJSON(path, data, function(data) {
		if(data.success) {
		    $('#competence-add-wrapper').append('<input type="hidden" name="3-key_competence_descriptions" value="'+data.competence_id+'">');
		}
	    });			  
	});
    });
}

$.ajaxSetup( { "async": false } );
$(make_dialogs);
