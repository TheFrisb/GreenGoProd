$(window).on("load", function () {
    $(".slider-holder").slick({
        infinite: true,
        arrows: true,
        adaptiveHeight: true,
        dots: true,
        speed: 200,
        
    });
    if(window.matchMedia("(min-width: 767px)").matches){
        $($(".slick-slide img").get().reverse()).each(function(i, el){
            if(!$(this).closest(".slick-slide").hasClass("slick-cloned")){
                $img = $(this).clone();
                if($(this).closest(".slick-slide").hasClass("slick-current")){
                    $img.addClass("active-gallery-item");
                    console.log("WAS")
                }
                $img.height(50); 
                $img.width(50);
                $img.prependTo($('.gallery-navigation'));
    
            }
        });
        gallery_navigation_images = $(".gallery-navigation img")
        $(".gallery-navigation img").on("click", function(){
            $(".gallery-navigation img").removeClass("active-gallery-item")
            $(".slider-holder").slick('slickGoTo', $(this).index());
            $(this).addClass("active-gallery-item");
        })
        $('.slider-holder').on('beforeChange', function(event, slick, currentSlide, nextSlide){
            $(gallery_navigation_images).removeClass("active-gallery-item")
            $(gallery_navigation_images[nextSlide]).addClass("active-gallery-item");
          });
    }
    $('.slider-holder').show();
    $("#overlay-loader").hide();
    $("#slider2").slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: true,
        speed: 300,
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
        speed: 300,
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
            currency: 'MKD',
            });
     })

