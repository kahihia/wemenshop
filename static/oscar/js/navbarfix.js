$(document).ready(function () {


	if($(window).width() > 767) {
		$('#logo-fullscreen').show();		
		$('#logo-smallscreen').hide();
		// console.log("window bigger than 767");
	} else {
		$('#logo-fullscreen').hide();
		$('#logo-smallscreen').show();
		// console.log("window smaller than 767");
	}
	console.log($(window).width());
});