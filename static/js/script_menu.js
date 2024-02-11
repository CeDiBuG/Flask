$(document).ready(function(){
  $(".preloader").fadeOut();
  $(".nav-link").click(function(e){
    var link = $(this).attr("href");
    $('html, body').animate({
      scrollTop: $(link).offset().top - 100
    }, 100);
    e.preventDefault();
  })
  $(".navbar").hide();
  $(".nav-icon, .navbar a, .nav-mask, .nav-toggle").click(function(e){
    $(".nav-icon").fadeToggle ();
    $(".navbar").fadeToggle(500);
  })
})
new WOW().init();

