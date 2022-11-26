
 $(document).ready(function() {
    console.log("Jquery loaded")

    function preventScroll(e){
        e.preventDefault();
        e.stopPropagation();
    
        return false;
    }

    const regular_price = parseInt($('.main-price').find('.product-regular-price').text());
    var cartCount = parseInt($("#cart-count").text())
    progress_bar = $('.progress__bar')

    console.log(cartCount)
    $("div#container").on('click', 'button.alert', function() {
        alert(1);
    });

    $(".header-menu").click(function (e){
        $(this).toggleClass("active");
        $("#navigation").toggleClass("active");
    })
    
    function toggleCart(){
        console.log("Cart Toggled")
        $('#sidecart').toggleClass('sidecart-active');
        $('.lightbox').toggleClass('lightbox-active')
    }
    function toggleSearch(){
        console.log("Search toggled")
        $('.lightbox').toggleClass('lightbox-active lightbox-search')
        $('.lightbox').find('form').toggleClass("disabled")
    }
    $('#search-mobile').click(function (e){
        toggleSearch()
    })
    $(".close-search").click(function (e){
        toggleSearch()
    })

    

    $('.header-cart').click(function (e){
        console.log("Cart Icon Clicked")
        if ($("#sidecart").hasClass('sidecart-active') == false){
            toggleCart();
        }

    })

    $('.cart-close').click(function (e){
        console.log("Cart Closed", "Cart close icon clicked")
        toggleCart();
    })


    $(".lightbox").click(function(){
        
        if ($("#sidecart").hasClass('sidecart-active')){
            console.log('yeas')
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
    $(document).on('click', '.add-to-cartBtn',function (e){
            
            
            button = $(this);
            e.stopPropagation();
            e.preventDefault();
            var product_id = $(this).closest('.product_data').find('.prod_id').val();
            var product_qty = $(this).closest('.product_data').find('.qty-input').val();
            var token = $('input[name=csrfmiddlewaretoken]').val()
            if (product_qty == null){
                product_qty = 1;
            }
            console.log($(button).hasClass("checkout-offerBtn"))
            
            $.ajax({
                method: "POST",
                url: "/add-to-cart",
                data: {
                    'product_id': product_id,
                    'product_qty': product_qty,
                    csrfmiddlewaretoken: token,
                },
                
                success: function (response){
                    if($(button).hasClass("sidecartOfferBtn")){
                        if($(button).hasClass("addedBtn") == false){
                            $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                            cartCount++;
                            $("#cart-count").html(cartCount)
                            $('.sidecart-inner').load(location.href + " .sidecart-inner");
                        }
                       
                        console.log(cartCount)
                        
                    }
                    else if($(button).hasClass("checkout-offerBtn")){
                        if($(button).hasClass("addedBtn") == false){
                            $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                        }
                        $('.cart-data').load(location.href + " .cart-data")
                        console.log('ADDED OFFER ITEM')
                    }
                    else if($(button).hasClass("proceed-to-checkout")){
                        window.location.href = "http://127.0.0.1:8000/checkout";
                    }
                    else {
                        if($(button).hasClass("mainaddedBtn") == false){
                            $(button).toggleClass('mainaddedBtn').html('ДОДАДЕН');
                            
                        }
                        cartCount = cartCount + parseInt(product_qty);
                        $("#cart-count").html(cartCount)
                        console.log(cartCount , product_qty)
                        $('.sidecart-inner').load(location.href + " .sidecart-inner");
                        toggleCart();
                    }
                }
            })
        
    })

    $(document).on('click', '.variable-add-to-cartBtn',function (e){
        
      button = $(this)
      var product_id = $(this).closest('.product_data').find('.prod_id').val();
      var product_qty = $(this).closest('.product_data').find('.qty-input').val();
      var selected_attribute = $(".product-attributes").find(".attribute-item.active");
      console.log("Attribute add to cart clicked for product id:", product_id, " with attribute id: ", attribute_id)
      var token = $('input[name=csrfmiddlewaretoken]').val()
      var attribute_id = 0;
      var attribute_type = null;
      if($(selected_attribute).length){
        attribute_id = $(selected_attribute).find(".attrib_id").val();
        attribute_type = $(selected_attribute).find(".attrib_type").val();
        $.ajax({
            method: "POST",
            url: "/variable-add-to-cart",
            data:{
                'product_id': product_id,
                'product_qty': product_qty,
                'attribute_id': attribute_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response){
                console.log("Attribute item successfully added")
                if($(button).hasClass("proceed-to-checkout")){
                    window.location.href = "http://127.0.0.1:8000/checkout";
                }
                else{
                    cartCount = cartCount + parseInt(product_qty);
                    $("#cart-count").html(cartCount)
                    console.log(cartCount , product_qty)
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                    $(button).html('ДОДАДЕН')
                    toggleCart();
                }
            }
        })
      }else{
        $(".attribute-title").css("color", "red");
      }


    })

    $(".offer-box").on('click', '.offer-button',function (e){
        button = $(this);
        if($(button).hasClass("addedBtn")){
            return 1;
        }
        e.stopPropagation();
        e.preventDefault();
        console.log('Thank you page order button clicked')
        var order_id = $(this).closest('.offer-box').find('.order_id').val();
        var product_id = $(this).closest('.offer-box').find('.prod_id').val();
        var product_qty = 1;
        var token = $('input[name=csrfmiddlewaretoken]').val()
        console.log('Order id:', order_id, 'Product id: ', product_id, 'product_qty', product_qty)
        
        $.ajax({
            method: "POST",
            url: "/add-to-order",
            data: {
                'order_id': order_id,
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                    $(button).addClass("addedBtn").html("ДОДАДЕН")
                    $('.cart-data').load(location.href + " .cart-data");

                
            }
        })
    })



    $('.sidecart-offer-item').on('click', 'sidecart-offer-item', function (e){
        console.log('offer clicked')
        e.preventDefault();
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
        $(".attribute-title").css("color", "#0f0f0f");
    })


    $(document).on('click', '.changeQuantity', function (e){
        e.preventDefault();
        console.log('click');
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var attribute_id = 0
        if($(this).closest('.product_data').find('.attrib_id').val() > 0){
            attribute_id = $(this).closest('.product_data').find('.attrib_id').val();
        }
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                'attribute_id': attribute_id,
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
        var cart_quantity = parseInt($(this).closest('.product_data').find(".sidecart-item-quantity").text());
        
        var attribute_id = 0
        if($(this).closest('.product_data').find('.attrib_id').val() > 0){
            attribute_id = $(this).closest('.product_data').find('.attrib_id').val();
        }
        console.log(attribute_id);
        var token = $('input[name=csrfmiddlewaretoken]').val()


        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                'attribute_id': attribute_id,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                if (window.location.href.indexOf("checkout") > -1){
                    $('.cart-data').load(location.href + " .cart-data")
                    $('.checkout-offers').load(location.href + " .checkout-offers")
                }
                else{
                    cartCount = cartCount - parseInt(cart_quantity)
                    
                    $('.sidecart-inner').load(location.href + " .sidecart-inner")
                    $("#cart-count").html(cartCount)
                }
                console.log('Deleted Successfully')
                
            }
        })
    })
    
    $(".checkout-fees").on('click', '.fee-toggle', function(e){
        e.preventDefault();
        $(this).find('.fee-icon').toggleClass('active');
        $(this).closest('.checkout-fees').find('.fee-description').slideToggle('next');
    })

    $(".checkout-fees").on('click', '.fee-add', function(e){
        e.preventDefault();
        button = $(this);
        fee_action = 'add';
        if($(this).closest('.checkout-fees').hasClass('active')){
            fee_action = 'remove';
        }
        console.log('Fee action:', fee_action)
        var fee_id = $(this).closest('.fee_data').find('.fee_id').val();
        console.log('Fee id:', fee_id)
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            method: "POST",
            url: "/add-or-delete-fee",
            data: {
                'fee_id': fee_id,
                'action': fee_action,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                console.log('Fee status changed to: ', fee_action)
                if($(button).closest('.checkout-fees').hasClass('active')){
                    $(button).toggleClass('addedBtn').html('ДОДАЈ');
                    $(button).closest('.checkout-fees').toggleClass('active');
                }else {
                    $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                    $(button).closest('.checkout-fees').toggleClass('active');
                }
                
                $('.cart-data').load(location.href + " .cart-data")   
                
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