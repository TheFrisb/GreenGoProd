$(window).on("load", function () {
    $(".slider-holder").slick({
        infinite: true,
        arrows: true,
        adaptiveHeight: true,
        dots: true,
        speed: 100,
        
    });
    $("#slider2").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: true,
        speed: 150,
        lazyLoad: 'ondemand',
        responsive: [
            {
            breakpoint: 1024,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1,
                infinite: true,
            }
            }]
    });
    $("#slider3").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: true,
        speed: 150,
        lazyLoad: 'ondemand',
        responsive: [
            {
            breakpoint: 1024,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1,
                infinite: true,
            }
            }]
    });
});
$(document).ready(function() {
        var elementPosition = $('.proceed-to-checkout').offset();
        $(window).scroll(function(){
                if($(window).scrollTop() > elementPosition.top){
                    $('.stickyBtn').slideDown();
                } else {
                    $('.stickyBtn').slideUp();
                }    
        });
        product_name = $('#main-product-title').text()
        product_price = $('#main-product-price').text()
        product_id = $('#main-product-id').val()
        fbq('track', 'ViewContent', {
            content_ids: [product_id],
            content_name: product_name,
            content_type: 'product',
            value: product_price,
            currency: 'USD'
            });
     })

