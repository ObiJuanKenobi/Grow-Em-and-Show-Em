// $(window).resize(function() {
	// var path = $(this);
	// var contW = path.width();
	// if(contW >= 751){
		// document.getElementsByClassName("sidebar-toggle")[0].style.left="200px";
	// }else{
		// document.getElementsByClassName("sidebar-toggle")[0].style.left="-200px";
	// }
// });
// $(document).ready(function() {
	// $('.dropdown').on('show.bs.dropdown', function(e){
	    // $(this).find('.dropdown-menu').first().stop(true, true).slideDown(300);
	// });
	// $('.dropdown').on('hide.bs.dropdown', function(e){
		// $(this).find('.dropdown-menu').first().stop(true, true).slideUp(300);
	// });
	// $("#menu-toggle").click(function(e) {
		// e.preventDefault();
		// var elem = document.getElementById("sidebar-wrapper");
		// left = window.getComputedStyle(elem,null).getPropertyValue("left");
		// if(left == "200px"){
			// document.getElementsByClassName("sidebar-toggle")[0].style.left="-200px";
		// }
		// else if(left == "-200px"){
			// document.getElementsByClassName("sidebar-toggle")[0].style.left="200px";
		// }
	// });
// });

$(document).ready(function () {
  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();      
    });

    function hamburger_cross() {

      if (isClosed == true) {          
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {   
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }
  
  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });  
});