 console.log("WOO")


//  const slidesContainer = document.getElementById("slides-container");
//  const slide = document.querySelector(".slide");
//  const prevButton = document.getElementById("slide-arrow-prev");
//  const nextButton = document.getElementById("slide-arrow-next");

//  nextButton.addEventListener("click", () => {
//    const slideWidth = slide.clientWidth;
//    slidesContainer.scrollLeft += slideWidth;
//  });

//  prevButton.addEventListener("click", () => {
//    const slideWidth = slide.clientWidth;
//    slidesContainer.scrollLeft -= slideWidth;
//  });

 $(document).ready(function() {
    const regular_price = parseInt($('.main-price').find('.product-regular-price').text());

    $("div#container").on('click', 'button.alert', function() {
        alert(1);
    });

    $(".header-search-icon").click(function (e){
        $(this).toggleClass("active");
        $("#navigation").toggleClass("active");
    })
    $("")
    
    function toggleCart(){
        $('#sidecart').toggleClass('sidecart-active');
        $('.lightbox').toggleClass('lightbox-active')
        console.log("was is das")
    }

    $('.sidecart-icon').click(function (e){
        toggleCart();
    })

    $('.cart-close').click(function (e){
        toggleCart();
    })


    $(".page-container").click(function(){
        if ($("#sidecart").hasClass('sidecart-active')){

            toggleCart();
        }
    })
    
    slide = $(".slide").innerWidth();
    slides_index_1 = 1;
    slides_index_2 = 1
    maxslides = slide * 8;
    $(".slider-wrapper1").on('click', '.slide-arrow', function(){
        slidescontainer = $(".slide-arrow-next1").next("ul");
        
        if($(this).hasClass('slide-arrow-next1')){
            console.log(slide*slides_index_1)
            slidescontainer.scrollLeft(slide * slides_index_1);
            slides_index_1++;
            console.log(slides_index_1);
            
        }
        if($(this).hasClass('slide-arrow-prev1')){
            slideleft = slide * (slides_index_1 - 1);         
            console.log(slideleft);
            slidescontainer.scrollLeft(slideleft - slide);
            if(slides_index_1 > 1){
                slides_index_1--;
            }
        }
        
    })
    $(".slider-wrapper2").on('click', '.slide-arrow', function(){
        slidescontainer = $(".slide-arrow-next2").next("ul");
        
        if($(this).hasClass('slide-arrow-next2')){
            console.log(slide*slides_index_2);
            
            slidescontainer.scrollLeft(slide * slides_index_2);
            slides_index_2++;
            console.log(slides_index_2);
            
        }
        if($(this).hasClass('slide-arrow-prev2')){
            slideleft = slide * (slides_index_2 - 1);         
            console.log(slideleft);
            slidescontainer.scrollLeft(slideleft - slide);
            if(slides_index_2 > 1){
                slides_index_2--;
            }
        }
        
    })


    // $('.increment-btn').click(function (e){
    $(document).on('click', '.increment-btn', function (e){
        e.preventDefault();
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0: value;
        
        value++;
        $(this).closest('.product_data').find('.qty-input').val(value);
        
    })

    $(document).on('click', '.decrement-btn', function (e){
        e.preventDefault();
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0: value;
        if( value > 1){
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    })
    $('.add-to-cartBtn').click(function (e){
        button = $(this);

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        print(product_id)
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        if (product_qty == null){
            product_qty = 1;
        }
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                if($(button).hasClass("proceed-to-checkout")){
                    window.location.href = "http://127.0.0.1:8000/checkout";
                }
                else {
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                    toggleCart();
                }
            }
        })
    })
    $('.product-attributes').on('click', '.attribute-item', function(){
        if($(this).hasClass('offer')){
            offer_regular_price = regular_price * ($(this).index());
            offer_price = parseInt($(this).find('.offer-price').text())
            $('.main-price').find('.product-regular-price').text(offer_regular_price + ' ден');
            $('.main-price').find('.product-sale-price').text(offer_price + ' ден');
        }   
        $('.product-attributes div').removeClass('active');
        $(this).toggleClass('active');
    })


    $(document).on('click', '.changeQuantity', function (e){
        e.preventDefault();
        console.log('click');
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        print(product_id)
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                console.log('Quantity changed NICE')
                $('.cart-data').load(location.href + " .cart-data")
            }
        })
    })
    

    $(document).on('click', '.remove-item', function (e){
       
        e.preventDefault()
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()


        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                if (window.location.href.indexOf("checkout") > -1){
                    $('.cart-data').load(location.href + " .cart-data")
                }
                else{
                    $('.sidecart-inner').load(location.href + " .sidecart-inner")
                }
                console.log('Deleted Successfully')
                
            }
        })
    })

    $(".toggle").click(function (e){
        console.log("Toggle click!")
        $(this).find(".toggle-content").slideToggle("fast");
    })
    $(".checkout-dostava").click(function (e){
        if($(".checkout-garancija").hasClass("active")){
            $(".checkout-garancija").removeClass("active");
            $(".checkout-garancija-content").slideToggle("fast");
        }
        $(this).toggleClass("active");
        $(".checkout-dostava-content").slideToggle("fast");
    })
    $(".checkout-garancija").click(function (e){
        if($(".checkout-dostava").hasClass("active")){
            $(".checkout-dostava").removeClass("active");
            $(".checkout-dostava-content").slideToggle("fast");
        }
        $(this).toggleClass("active");
        $(".checkout-garancija-content").slideToggle("fast");
    })
 })