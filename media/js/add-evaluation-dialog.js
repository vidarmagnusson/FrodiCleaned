function make_dialog() {
	$('.dialog-add-form').each(function (index) {
		$(this).dialog({
		autoOpen: false,
		height: 200,
		width: 460,
		modal: true,
		buttons: {
			"Senda inn": function() {
				var status = false;
				var this_id = $(this).attr('id').replace('_add-form','');
				var this_number = this_id.replace('_goal','');
				var path = '/api/namskra/framhaldsskolar/evaluation/new/';
				if (this_number != 'none') {
					path += 'goal/'+this_number+'/'
				}
				var data = { q:$('#'+this_id+'_input').val() };
				$.post(path, data, function(data) {
					if (data.success) {
						$('.evaluation_values').val($('.evaluation_values').val()+data.id+',');
						$('#'+this_id+'_added').html( $('#'+this_id+'_added').html()+'<li id="'+this_id+'_item'+data.id+'">'+$('#'+this_id+'_input').val()+'</li>');
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
			},
		close: function() {
			allFields.val( "" ).removeClass( "ui-state-error" );
		}
		});
	});

	$(".add-to-list").click(function(event) {
		var dialog_id = '#' + $(this).attr('id') + '-form';
		$(dialog_id).dialog( "open" );
		event.preventDefault();
	});
}

$.ajaxSetup( { "async": false } );
$(make_dialog);
