function make_dialogs() {
    $('.delete-goal').live('click', function(event) {
	var list_element = $(this).parent();
	var goal_id = (list_element.attr('class')).replace('goal_','');
	$('#goal_text').html(list_element.text());
	$('#goal_to_delete').val(goal_id);
	$('#confirm-delete-dialog').dialog('open');
    });

    $('#confirm-delete-dialog').dialog({
	autoOpen: false,
	height:250,
	modal: true,
	buttons: {
	    "Eyða markmiði": function() {
		var post_form = $('#delete-goal_form');
		$.post(post_form.attr('action'), post_form.serialize(), function(data) {
		    if (data.success) {
			var remove_class = '.goal_'+$('#goal_to_delete').val();
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
    
    $('.dialog-add-form').each(function (index) {
	$(this).dialog({
	    autoOpen: false,
	    height: 400,
	    width: 460,
	    modal: true,
	    buttons: {
		"Senda inn": function() {
		    var status = false;
		    var this_id = $(this).attr('id').replace('_add-form','');
		    if ($('#'+this_id+'_input').val() == '') { return false; }
		    var post_form = $('#'+this_id+'_form');
		    $.post(post_form.attr('action'), post_form.serialize(), 
			   function(data) {
			       if (data.success) {
				   var goal = $('#'+this_id+'_input').val() +' <img class="delete-goal" src="/media/icons/eyda.png" alt="Eyða markmiði">';

				   if (data.evaluation_id) {
				       var evaluation = $('#'+this_id.replace('goals','evaluation'));
				       goal = goal + '<ul><li class="goal_evaluation'+data.evaluation_id+'"><div><em>Námsmat</em></div>'+evaluation.val()+'</li></ul>';
				       evaluation.val('');
				   }
			       
				   $('#'+this_id+'_wrapper').append('<input type="hidden" value="'+data.goal_id+'" name="'+this_id+'" id="id_'+this_id+'_'+data.goal_id+'" class="goal_'+data.goal_id+'" />');
				   $('#'+this_id+'_added').append('<li id="item_'+this_id+'_'+data.goal_id+'" class="goal_'+data.goal_id+'">'+goal+'</li>');
				   $('#'+this_id+'_input').val('');
		
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
    });
    
    $(".add-to-list").click(function(event) {
	var dialog_id = '#' + $(this).attr('id') + '-form';
	$(dialog_id).dialog('open');
	event.preventDefault();
    });
}

$.ajaxSetup( { "async": false } );
$(make_dialogs);
