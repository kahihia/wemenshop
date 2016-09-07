$(document).ready(function() {
	$( "#cart-show-hide-button" ).click(function() {
	 	
	 	$('#cart_content').toggle();
	 	$('#basket-arrow-up').toggle();
	 	$('#basket-arrow-down').toggle();

	 	if($('#cart_content').is(":visible")) {
			Cookies.set('cartVisible', 'true');
		} else {
			Cookies.set('cartVisible', 'false');
		}
	});

	$('.btn-add-to-basket').click( function () {
		$('#cart_content').show();
	 	$('#basket-arrow-up').show();
	 	$('#basket-arrow-down').hide();

	 	if($('#cart_content').is(":visible")) {
			Cookies.set('cartVisible', 'true');
		} else {
			Cookies.set('cartVisible', 'false');
		}
	});
	

	if (Cookies.get('cartVisible') == 'true') {
		$('#cart_content').show();
	 	$('#basket-arrow-up').show();
	 	$('#basket-arrow-down').hide();
	 } else {
	 	$('#cart_content').hide();
	 	$('#basket-arrow-up').hide();
	 	$('#basket-arrow-down').show();
	 }
	 console.log(Cookies.get('cartVisible'));
});
