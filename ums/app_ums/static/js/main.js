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
	if ( $('#registration_container')){
		// if($('#form_title').html() == 'SignIn'){
			$('#sign-in-container').addClass('registration_me_on_front');
			$('#sign-up-container').addClass('registration_me_on_back');
			$('#signUp')
				.on('click', function(){
					$('#registration_container').addClass('right-panel-active');
				})
			$('#signIn')
			.on('click', function(){
				$('#registration_container').removeClass('right-panel-active');
			})
		// }else{	// signUp
		// 	$('#sign-up-container').addClass('registration_me_on_front');
		// 	$('#sign-in-container').addClass('registration_me_on_back');
		// 	$('#signIn')
		// 		.on('click', function(){
		// 			$('#registration_container').removeClass('right-panel-active');
		// 		})
		// 		$('#signUp')
		// 	.on('click', function(){
		// 		$('#registration_container').addClass('right-panel-active');
		// 	})
		// }
		//FIXME: couldnt fix this animation for dynamic rendering on signin & signup
	}

    
    $('#forgot-pwd-a')
        .on('click',function(){
            $('#sing-in-form').addClass('hidden');
            $('#forgot-pwd-form').removeClass('hidden');
        })

    $('#back-to-login-form-a')
        .on('click',function(){
            $('#sing-in-form').removeClass('hidden');
            $('#forgot-pwd-form').addClass('hidden');
		})
		
	//---------------------------- SignUp: Handled by stripe-jsfiles.js
	//---------------------------- login
	$('#signin-form')
		.on('submit',function(evt){ 		//TODO: add form validation here
			evt.preventDefault();		//this fucker costted me 6 hours & a sleep break ARGGHHHH
			submitSignInForm().then((result)=>{
				if (result.message == "user logged in successfully"){
					window.location.href = '/dashboard'
				}else{
					alert(result.message);
				}
			})
		})

	function submitSignInForm(){
		let email = document.querySelector('#signin_email').value;
		let password = document.querySelector('#signin_password').value;
		let csrf_token = document.querySelector('#signin_csrf_token').value;

		return fetch('/signin', {
				method: 'post',
				headers: {
					'X-CSRFToken': csrf_token, 
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					email: email,
					password: password
				}),
			})  
			.then((response) => {
				return response.json();
			})
			.then((result) => {
				// console.log("result: ",result);
				return result;
			});
	}
	//----------------------------forget pwd
	$('#forgetpwd-form')
		.on('submit',function(evt){
			evt.preventDefault();
			submitForgetPwdForm().then((result)=>{
				if (result.message == "user found and mail sent"){
					window.location.href = '/forgetpwdprocess/success'
				}else if (result.message == "user not found"){
					window.location.href = '/forgetpwdprocess/foreigner'
				}else{
					alert(result.message);
				}
			})

		})
	
	function submitForgetPwdForm(){
		let email = document.querySelector('#forgetpwd_email').value;
		let csrf_token = document.querySelector('#forgetpwd_csrf_token').value;

		return fetch('/forgetpwd', {
				method: 'post',
				headers: {
					'X-CSRFToken': csrf_token, 
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					email: email
				}),
			})  
			.then((response) => {
				return response.json();
			})
			.then((result) => {
				// console.log("result: ",result);
				return result;
			});
	}

	//----------------------------reset pwd
	$('#resetpwd-form')
		.on('submit',function(evt){
			console.log("here in reset");
			evt.preventDefault();

			let password = document.querySelector('#reset_password').value;
			let password_confirm = document.querySelector('#reset_password_confirm').value;
			if(password != password_confirm){
				let errmsg = document.createElement('p');
				errmsg.innerHTML = "Passwords dont match";
				document.getElementById("reset_err_msg").appendChild(errmsg);
			}else{
				submitResetPwdForm().then((result)=>{
					if (result.message == "user password updated successfully"){
						window.location.href = '/signup'
					}else{
						alert(result.message);
					}
				})
			}
		})
	
	function submitResetPwdForm(){
		let password = document.querySelector('#reset_password').value;
		let csrf_token = document.querySelector('#reset_csrf_token').value;
		var token = window.location.href.split('/').slice(-1)[0] 		//hack to get token from url

		return fetch('/resetpwd/'+token, {
				method: 'post',
				headers: {
					'X-CSRFToken': csrf_token, 
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					password: password
				}),
			})  
			.then((response) => {
				return response.json();
			})
			.then((result) => {
				// console.log("result: ",result);
				return result;
			});
	}
    
    // ============================ Registration Form:END =====================
    
    // ============================ Pricing Page:START =====================
    $('#pricing-btn-basic')
        .on('click',function(){
			$('#card_details').removeClass('hidden');
			$('#pricing-btn-basic').text = 'Selected';
        })
		
	$('#pricing-btn-premium')
        .on('click',function(){
			$('#card_details').removeClass('hidden');
			$('#pricing-btn-premium').text = 'Selected';
        })
    // ============================ Pricing Page:END =====================

})(jQuery);



