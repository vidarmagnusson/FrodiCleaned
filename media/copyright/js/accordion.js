function init_jquery_effects() {
	$('.collapse-text').hide();

	$('.collapse-header').click(function() {		
		$(this).siblings('.collapse-text').slideToggle('slow');
	});

	$('.collapse-text:first').slideDown('slow');
}

function scroll_around() {
	$('a[href*=#]').click(function() {
		var duration=1000;
		var easing='swing';

		// get / set parameters
		var newHash=this.hash;
		
		if ($(newHash).hasClass('collapse-header')) {
			if ($(newHash).siblings('.collapse-text').is(':hidden')) {
				$(newHash).siblings('.collapse-text').slideDown('slow');
			}
		}

		var target=$(this.hash+', a[name='+this.hash.slice(1)+']').offset().top - 30;
		var oldLocation=window.location.href.replace(window.location.hash, '');
		var newLocation=this;

      		// make sure it's the same location      
		if(oldLocation+newHash==newLocation)
      		{
			//if($.browser.safari) var animationSelector='body:not(:animated)';
			//else var animationSelector='html:not(:animated)';
			var animationSelector='html:not(:animated)';

			// animate to target and set the hash to the window.location after the animation
			$(animationSelector).animate({ scrollTop: target }, duration, easing, function() {
	            		// add new hash to the browser location
				//window.location.href=newLocation;
			});

			// cancel default click action
			return false;
		}
	});
}

$(init_jquery_effects);
$(scroll_around);

