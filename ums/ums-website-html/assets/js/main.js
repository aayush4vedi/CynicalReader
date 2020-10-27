/* =============================== HOME PAGE: index.html ========================*/

(function($) {

    // ============================ Home Page:START =====================

	var	$window = $(window),
		$body = $('body'),
		$wrapper = $('#page-wrapper'),
		$banner = $('#banner'),
		$header = $('#header');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ null,      '480px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Mobile?
		if (browser.mobile)
			$body.addClass('is-mobile');
		else {

			breakpoints.on('>medium', function() {
				$body.removeClass('is-mobile');
			});

			breakpoints.on('<=medium', function() {
				$body.addClass('is-mobile');
			});

		}

	// Scrolly.
		$('.scrolly')
			.scrolly({
				speed: 1500,
				offset: $header.outerHeight()
			});

	// Menu.
		$('#menu')
			.append('<a href="#menu" class="close"></a>')
			.appendTo($body)
			.panel({
				delay: 500,
				hideOnClick: true,
				hideOnSwipe: true,
				resetScroll: true,
				resetForms: true,
				side: 'right',
				target: $body,
				visibleClass: 'is-menu-visible'
            });
            
	// Header.
		if ($banner.length > 0
		&&	$header.hasClass('alt')) {

			$window.on('resize', function() { $window.trigger('scroll'); });

			$banner.scrollex({
				bottom:		$header.outerHeight() + 1,
				terminate:	function() { $header.removeClass('alt'); },
				enter:		function() { $header.addClass('alt'); },
				leave:		function() { $header.removeClass('alt'); }
			});

        }
    // ============================ Home Page:END =====================
        
    // ============================ Registration Form:START ===================
    // Click on SignUp Button/Buy Button => Make Login form visible
    $('#signUp')
        .on('click', function(){
            $('#registration_container').addClass('right-panel-active');
        })
    $('#signIn')
        .on('click', function(){
            $('#registration_container').removeClass('right-panel-active');
        })
    
    $('#forgot-pwd-a')
        .on('click',function(){
            console.log("ouchhhhhhhh");;
            $('#sing-in-form').addClass('hide-me');
            $('#forgot-pwd-form').removeClass('hide-me');
        })

    $('#back-to-login-form-a')
        .on('click',function(){
            console.log("ouchhhhhhhh");;
            $('#sing-in-form').removeClass('hide-me');
            $('#forgot-pwd-form').addClass('hide-me');
        })
    
    // Click on SignUp Button/Buy Button => Make SingUp form visible

    // ============================ Registration Form:END =====================
    
    // ============================ Pricing Page:START =====================
    $('#pricing-btn-basic')
        .on('click',function(){
            $('#card_details').removeClass('hide-me');
        })

    $('#pricing-btn-premium')
        .on('click',function(){
            $('#card_details').removeClass('hide-me');
        })
    // ============================ Pricing Page:END =====================

})(jQuery);


