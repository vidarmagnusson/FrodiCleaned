function make_draggable() {
  $('.draggable-course').draggable({
      cursor: 'move',
      opacity: 0.7,
      scroll: true,
      containment: 'document',
      helper: 'clone'
  });

    $('.bound-package-list').each(function() {
	var bound = $(this)
	var packages = bound.attr('packages').split(',');
	$.each(packages, function() {
	    bound.append('<div class="package"><div class="title">Pakki: '+this+'</div><ul class="list"></ul><div class="package-add">Dragðu áfanga hingað til að bæta við</div></div>');
	});

    });


  $('.new-package').droppable( {
      hoverClass: 'package-hover',
      drop: function(event, ui) {
	  var draggable = ui.draggable;
	  $(this).siblings('.package-list').append('<div class="package"><div class="title">Pakki: '+draggable.text()+'</div><ul class="list"><li>'+draggable.text()+'</li></ul><div class="package-add">Dragðu áfanga hingað til að bæta við</div></div>');

	  $('.package-add').droppable( {
	      hoverClass: 'package-hover',
	      drop: function(event, ui) {
		  var draggable = ui.draggable;
		  $(this).siblings('.list').append('<li>'+draggable.text()+'<li>');
	      }
	  });
      }
  });
}

$.ajaxSetup( { "async": false } );
$(make_draggable);
