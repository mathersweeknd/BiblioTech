// Rolagem Suave

$('a[href="#top"]').on('click', function (event) {
    event.preventDefault();
    $('html, body').animate({ scrollTop: 0 }, 1500);
});

$('a[href^="#"]').on('click', function (event) {
    event.preventDefault();
    var target = $(this.getAttribute('href'));
    if (target.length) {
        $('html, body').animate({
            scrollTop: target.offset().top
        }, 1500);
    }});

    