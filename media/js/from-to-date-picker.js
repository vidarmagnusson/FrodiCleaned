function create_datepickers() {
	var dates = $( "#start_date_day, #end_date_day" ).datepicker({
		defaultDate: "+1d",
		changeMonth: true,
		numberOfMonths: 1,
		onSelect: function( selectedDate ) {
			var option = this.id == "start_date_day" ? "minDate" : "maxDate",
			instance = $( this ).data( "datepicker" ),
			date = $.datepicker.parseDate(
				instance.settings.dateFormat ||
				$.datepicker._defaults.dateFormat,
				selectedDate, instance.settings );
			dates.not( this ).datepicker( "option", option, date );
		}
	});

	$('form:first').submit(function() {
		var start_day = $('#start_date_day').val();
		var start_time = $('#start_date_time').val();
		var end_day = $('#end_date_day').val();
		var end_time = $('#end_date_time').val();

		if ((start_day == '') || (start_time == '')) {
			return false;
		}
		if (start_time.length == 1) { start_time = '0'+start_time+':00'}
		if (start_time.length == 2) { start_time = start_time+':00'}
		if (start_time.length != 5) { return false; }
		
		$('#id_start_date').val(start_day+' '+start_time);

		if ((end_day == '') || (end_time == '')) {
			return false;
		}
		if (end_time.length == 1) { start_end = '0'+end_time+':00'}
		if (end_time.length == 2) { start_end = end_time+':00'}
		if (end_time.length != 5) { return false; }
		
		$('#id_end_date').val(end_day+' '+end_time);
	});
}

$.ajaxSetup( { "async": false } );
$(create_datepickers);
