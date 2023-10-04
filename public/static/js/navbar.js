$(window).on("scroll", function() {
    var navbarr = $(".navbarr");
    if ($(window).scrollTop() > 0) {
      navbarr.addClass("scroll");
    } else {
      navbarr.removeClass("scroll");
    }
});