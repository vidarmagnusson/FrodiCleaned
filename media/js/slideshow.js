/**
 * Slideshow based on the simple and straightforward slideshow
 * Jon Raasch showed here: http://jonraasch.com/blog/a-simple-jquery-slideshow
 */

// Slide switching function
function switch_slides() {
    // Get the current active slide
    var active_slide = $('#slideshow .active');

    // Set the default active slide to the last one to avoid flicker
    if ( active_slide.length == 0 ) {
	active_slide = $('#slideshow .slide:last');
    }

    // Get the next slide and if there isn't a next slide get the first one
    // to create a looping slideshow
    var next_slide =  active_slide.next().length ? active_slide.next()
        : $('#slideshow .slide:first');

    // The current active slide should now be marked as the last active (since
    // we are about to switch slides)
    active_slide.addClass('last-active');

    // We then set the next slide opacity to 0 (transparent), add to it the
    // active class (mark it) and then animate it's opacity change (fade in).
    // After the animation is done we remove the active and the last-active
    // class from the current active slide (since now the active slide is the
    // next slide and we're done
    next_slide.css({opacity: 0.0})
	.addClass('active')
	.animate({opacity: 1.0}, 2000, function() {
            active_slide.removeClass('active last-active');
        });
}

// Function which takes care of setting the interval of the slide switching
function slideshow() {
    // We start the slide switching by default at 30 seconds per slide
    var slide_switcher = setInterval('switch_slides()', 30000);

    // If the visitor hovers over the slide we clear the interval since we
    // want hovering to be a 'pause this slideshow' event. When the visitor
    // leaves the slide we set the interval again at 30 seconds
    $('#slideshow').hover(function() { clearInterval(slide_switcher); },
			  function() {
			      slide_switcher = setInterval('switch_slides()',
							   30000 );
			  });
}

// Lambda function that runs the slideshow
$(function() {
    slideshow();
});
