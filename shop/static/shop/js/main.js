 $(document).ready(function() {

    const regular_price = parseInt($('.main-price').find('.product-regular-price').text());
    const sale_price = parseInt($('.main-price').find('.product-sale-price').text());
    const money_saved = $('.main-price').find('.money_saved').text()
    const percentage = $('.main-price').find('.percentage').text()
    const attrib_heading = $('.product-attributes').find('.attribute-title').text();
    var cartCount = parseInt($("#cart-count").text())

    $("div#container").on('click', 'button.alert', function() {
        alert(1);
    });

    $(".header-menu").click(function (e){
        $(this).toggleClass("active");
        $("#navigation").toggleClass("active");
    })
    
    function toggleCart(){
        $('#sidecart').toggleClass('sidecart-active');
        $('.lightbox').toggleClass('lightbox-active')
    }
    function toggleSearch(){
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
        if ($("#sidecart").hasClass('sidecart-active') == false){
            toggleCart();
        }

    })

    $('.cart-close').click(function (e){
        toggleCart();
    })


    $(".lightbox").click(function(){
        
        if ($("#sidecart").hasClass('sidecart-active')){
            toggleCart();
        }
    })
    
    // slide = $(".slide").innerWidth();
    slide1 = $(".slider-wrapper1").find(".slide").innerWidth();
    slide2 = $(".slider-wrapper2").find(".slide").innerWidth();
    var slides_index_1 = 1;
    var slides_index_2 = 1
    var maxslides1 = $(".slider-wrapper1").find(".slide").length
    var maxslides2 = $(".slider-wrapper2").find(".slide").length
    $(".slider-wrapper1").on('click', '.slide-arrow', function(){
        slidescontainer = $(".slide-arrow-next1").next("ul");
        if($(this).hasClass('slide-arrow-next1')){
           
            slidescontainer.scrollLeft(slide1 * slides_index_1);
            if((slide1>220 && slides_index_1 <( maxslides1 - 3)) || slide1<220 && slides_index_1 <( maxslides1 - 1)){
                
                slides_index_1++;
            }
            
        }
        if($(this).hasClass('slide-arrow-prev1')){
            slideleft = slide1 * (slides_index_1 - 1);         
            slidescontainer.scrollLeft(slideleft - slide1);
            if(slides_index_1 > 1){
                slides_index_1--;
            }
        }
        
    })
    $(".slider-wrapper2").on('click', '.slide-arrow', function(){
        slidescontainer = $(".slide-arrow-next2").next("ul");
        
        if($(this).hasClass('slide-arrow-next2')){
 
            
            slidescontainer.scrollLeft(slide2 * slides_index_2);
            if((slide2>220 && slides_index_2 <( maxslides2 - 3)) || slide2<220 && slides_index_2 <( maxslides2 - 1)){
                slides_index_2++;
                }
            
        }
        if($(this).hasClass('slide-arrow-prev2')){
            slideleft = slide2 * (slides_index_2 - 1);         
            slidescontainer.scrollLeft(slideleft - slide2);
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
            $(this).find('.load-spinner').css('display', 'inline-block');
            $(this).find('.btn-text').css('display', 'none');
            var product_id = $(this).closest('.product_data').find('.prod_id').val();
            var product_qty = $(this).closest('.product_data').find('.qty-input').val();
            var productPrice = $(this).closest('.product_data').find(".product-price-tracker").text()
            var productName = $(this.closest('.product_data')).find('.prod_title_tracker').text()
            var token = $('input[name=csrfmiddlewaretoken]').val()
            if (product_qty == null){
                product_qty = 1;
            }
            if($(button).hasClass("stickyBtn")){
                var product_id = $('.product-page.product_data').find('.prod_id').val();
                var product_qty = $('.product-page.product_data').find('.qty-input').val();
                if (product_qty == null){
                    product_qty = 1;
                }
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
                    if($(button).hasClass("sidecartOfferBtn")){
                        if($(button).hasClass("addedBtn") == false){
                            $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                            cartCount++;
                            $("#cart-count").html(cartCount)
                            $('.sidecart-inner').load(location.href + " .sidecart-inner");
                        }
                       
                      
                    }
                    else if($(button).hasClass("checkout-offerBtn")){
                        if($(button).hasClass("addedBtn") == false){
                            $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                        }
                        $('.cart-data').load(location.href + " .cart-data")
                    }
                    else if($(button).hasClass("proceed-to-checkout")){
                        window.location.href = "/checkout/";
                    }
                 
                    else {
                        cartCount = cartCount + parseInt(product_qty);
                        $("#cart-count").html(cartCount)
                        $('.sidecart-inner').load(location.href + " .sidecart-inner");
                        if($(button).hasClass("mainaddedBtn") == false){
                            setTimeout(() => {
                                $(button).toggleClass('mainaddedBtn').html('ДОДАДЕН');
                                toggleCart();
                              }, 250)
                            }
                        else{
                            toggleCart()
                        }
                    }

                }
            })
        
    })

  
    $(document).on('click', '.offerBtn',function (e){
        e.stopPropagation();
        e.preventDefault();
            
        button = $(this);
        if($(button).hasClass('addedBtn')){
            return;
        }
       

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = 1;
        var product_price = $(this).closest('.product_data').find('.offer_price').val();
        var productName = $(this.closest('.product_data')).find('.prod_title_tracker').text()
        var token = $('input[name=csrfmiddlewaretoken]').val()
        if (product_qty == null){
            product_qty = 1;
        }
        
        $.ajax({
            method: "POST",
            url: "/offer-add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                'product_price': product_price,
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
                    
                }
                else if($(button).hasClass("checkout-offerBtn")){
                    if($(button).hasClass("addedBtn") == false){
                        $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                    }
                    $('.cart-data').load(location.href + " .cart-data")
                }

            }
        })
    
    })
  
    $(document).on('click', '.variable-add-to-cartBtn',function (e){
        
      button = $(this)
      var product_id = $(this).closest('.product_data').find('.prod_id').val();
      var product_qty = $(this).closest('.product_data').find('.qty-input').val();
      var selected_attribute = $(".product-attributes").find(".attribute-item.active");
      var productName = $(this.closest('.product_data')).find('.prod_title_tracker').text()
      var token = $('input[name=csrfmiddlewaretoken]').val()
      var attribute_id = 0;
      var attribute_type = null;
      if (product_qty == null){
         product_qty = 1;
       }
       if($(button).hasClass("stickyBtn")){
         var product_id = $('.product-page.product_data').find('.prod_id').val();
         var product_qty = $('.product-page.product_data').find('.qty-input').val();
         if (product_qty == null){
             product_qty = 1;
         }
       }
      if($(selected_attribute).length){
        attribute_id = $(selected_attribute).find(".attrib_id").val();
        attribute_type = $(selected_attribute).find(".attrib_type").val();
        product_price = $('.main-price').find('.product-price-tracker').text()
        $(this).find('.load-spinner').css('display', 'inline-block');
        $(this).find('.btn-text').css('display', 'none');
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
                if($(button).hasClass("proceed-to-checkout")){
                    window.location.href = "/checkout/";
                }
                else{
                    cartCount = cartCount + parseInt(product_qty);
                    $("#cart-count").html(cartCount)
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                    if($(button).hasClass("mainaddedBtn") == false){
                        setTimeout(() => {
                            $(button).toggleClass('mainaddedBtn').html('ДОДАДЕН');
                            toggleCart();
                            }, 250)
                        }
                    else{
                        toggleCart()
                    }
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
        var order_id = $(this).closest('.offer-box').find('.order_id').val();
        var product_id = $(this).closest('.offer-box').find('.prod_id').val();
        var product_qty = 1;
        var token = $('input[name=csrfmiddlewaretoken]').val()
        
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
        e.preventDefault();
    })
    $('.product-attributes').on('click', '.attribute-item', function(){
        attrib_title = ': ' + $(this).find('.attrib_title').val();
        if($(this).hasClass('offer')){
            offer_regular_price = regular_price * ($(this).index());
            offer_price = parseInt($(this).find('.offer-price').text())
            $('.main-price').find('.product-regular-price').text(offer_regular_price + ' ден');
            $('.main-price').find('.product-price-tracker').text(offer_price);
            if($(this).index()!=1){
                $('.main-price').find('.money_saved').text(parseInt(offer_regular_price - offer_price))
                $('.main-price').find('.percentage').text('-' + parseInt(100 - (offer_price / offer_regular_price * 100)) + '%')
            }
            else{
                $('.main-price').find('.money_saved').text(money_saved)
                $('.main-price').find('.percentage').text(percentage)
            }
        }
        else{
            offer_price = $(this).find('.attrib_price').val();
            if(sale_price != offer_price){
            offer_regular_price = regular_price * ($(this).index());
            $('.main-price').find('.product-regular-price').text(offer_regular_price + ' ден');
            $('.main-price').find('.money_saved').text(parseInt(offer_regular_price - offer_price))
            $('.main-price').find('.percentage').text('-' + parseInt(100 - (offer_price / offer_regular_price * 100)) + '%')
            }
            else{
                offer_regular_price = regular_price
                $('.main-price').find('.product-regular-price').text(offer_regular_price + ' ден');
                $('.main-price').find('.money_saved').text(money_saved)
                $('.main-price').find('.percentage').text(percentage)
            }
            $('.main-price').find('.product-price-tracker').text(offer_price);
        }
        $('.product-attributes div').removeClass('active');
        $(this).toggleClass('active');
        $(".attribute-title").text(attrib_heading + attrib_title);
        $(".attribute-title").css("color", "#0f0f0f");
    })


    $(document).on('click', '.changeQuantity', function (e){
        e.preventDefault();
        button = $(this);
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
                if($(button).hasClass('sidecart-qty')){
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                }
                else{
                    $('.cart-data').load(location.href + " .cart-data")
                }
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
        var token = $('input[name=csrfmiddlewaretoken]').val()
        var cart_items_count = $('#cart_items_count').val()

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
                    if(cart_items_count == 1){
                        $(".content-container.checkout").remove();
                        $(".page-container").append('<div class="content-container checkout"><div class="no-cart"><h2 class="no-cart-title">Немате производи во кошничка</h2><a href="/" class="no-cartBtn">Врати ме на почетна</a></div></div>');
                    }
                }
                else{
                    cartCount = cartCount - parseInt(cart_quantity)
                    
                    $('.sidecart-inner').load(location.href + " .sidecart-inner")
                    $("#cart-count").html(cartCount)
                }
                
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
        var fee_id = $(this).closest('.fee_data').find('.fee_id').val();
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
    

    $(".toggle-title").click(function (e){
        $(this).next(".toggle-content").slideToggle("fast");
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
  
   function myFunction() {
        var min = 13,
          max = 20;
        var rand = Math.floor(Math.random() * (max - min + 1) + min); //Generate Random number between 5 - 10
        var minutes_ago = Math.floor(Math.random() * (58 - 2 + 1) + 1)
        const names = ["Александар","Ангела","Марија","Елена",
        "Здравко","Зорица","Костадин","Живка","Никола","Ева",
        "Наум","Филип","Бранкица","Мартин","Ивана",
        "Ристе","Лилјана","Борис","Ефимија","Живко",
        "Христина","Васил"];
        var name = names[Math.floor(Math.random()*names.length)];
        $.ajax({
            url: "/get_recent_ordered",
            type: 'GET',
            dataType: 'json', // added data type
            success: function(res) {
                $("#ordered_items_notice").attr("href", res.url);
                $("#ordered_product_thumbnail").attr("src", res.thumbnail);
                $("#order_person_name").html(name);
                $("#order_person_product_name").html(res.title);
                $("#order_product_regular_price").html(res.regular_price);
                $("#order_product_sale_price").html(res.sale_price);
                $("#ordered_items_notice_wrapper").fadeToggle(400);
                $("#order_time_minutes_ago").html(minutes_ago);
                setTimeout(function () {
                    $("#ordered_items_notice_wrapper").fadeOut(400);
                }, 5000);
                }
        });
        

        setTimeout(myFunction, rand * 1000);
    }   
    if($("#ordered_items_notice_wrapper")){
        $(document).on('click','#close_ordered_items_notice', function(e){
            e.preventDefault();
            $("#ordered_items_notice_wrapper").fadeOut(200);
        })
        setTimeout(myFunction, (Math.floor(Math.random() * (20 - 13 + 1) + 13)) * 1000)
    }
 })
