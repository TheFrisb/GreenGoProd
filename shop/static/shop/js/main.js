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
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                    $('.checkout-form-inner').load(location.href + " .checkout-form-inner");
                    cartCount++;
                    $("#cart-count").html(cartCount)
                    if($(button).hasClass("hasUpsells")){
                        console.log('called 1')
                        $(".product-page-upsell").each(function(i, obj){
                            if($(this).hasClass("checked")){
                                var image = $(this).find(".product-upsell-image").attr('src')
                                var price = $(this).find(".product-upsell-price-data").val();
                                var product_id = $(this).find(".product-upsell-product-id").val();
                                var upsell_name = $(this).find(".product-upsell-title-data").val();
                                var upsell_id = $(this).find(".product-upsell-data-id").val()
                                $.ajax({
                                    method: "POST",
                                    url: "/add-upsell-to-cart",
                                    data: {
                                        'product_id': product_id,
                                        'price': price,
                                        'image_url': image,
                                        'upsell_name': upsell_name,
                                        'upsell_id': upsell_id,
                                        csrfmiddlewaretoken: token,
                                    },
                                    success: function (response){
                                        $('.sidecart-inner').load(location.href + " .sidecart-inner");
                                        $('.checkout-form-inner').load(location.href + " .checkout-form-inner")
                                    }
                                })

                                
                            }
                        })


                    }
                    if($(button).hasClass("sidecartOfferBtn")){
                        if($(button).hasClass("addedBtn") == false){
                            $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                        }
                        else{
                            toggleCart()
                        }
                       
                    }
                    else if($(button).hasClass("proceed-to-checkout")){

                        $("#checkout_form_overlay").toggle();
                        $('body').toggleClass("checkout-is-active");
                        $.ajax({
                            method: "POST",
                            url: "/call-pixel-checkout",
                            data: {
                                csrfmiddlewaretoken: token,
                            },
                        })
                    }

                    else{     
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

        if($(this).hasClass("checkout-offer")){
            var product_id = $(this).siblings('.prod_id').val();
            var product_qty = 1;
            var product_price = $(this).siblings('.offer_price').val();
            console.log(product_id, product_price)

        }

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
                cartCount++;
                $("#cart-count").html(cartCount)
                if($(button).hasClass("sidecartOfferBtn")){
                    if($(button).hasClass("addedBtn") == false){
                        $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                    }
                }
                else if($(button).hasClass("add-upsell")){
                    if($(button).hasClass("addedBtn") == false){
                        $(button).toggleClass('addedBtn').html('ДОДАДЕН');
                    }
                }
                $('.sidecart-inner').load(location.href + " .sidecart-inner");
                $('.checkout-form-inner').load(location.href + " .checkout-form-inner");

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
                cartCount = cartCount + parseInt(product_qty);
                    $("#cart-count").html(cartCount)
                    $('.sidecart-inner').load(location.href + " .sidecart-inner");
                    $('.checkout-form-inner').load(location.href + " .checkout-form-inner");
                if($(button).hasClass("hasUpsells")){
                        console.log('called 1')
                        $(".product-page-upsell").each(function(i, obj){
                            if($(this).hasClass("checked")){
                                var image = $(this).find(".product-upsell-image").attr('src')
                                var price = $(this).find(".product-upsell-price-data").val();
                                var product_id = $(this).find(".product-upsell-product-id").val();
                                var upsell_name = $(this).find(".product-upsell-title-data").val();
                                var upsell_id = $(this).find(".product-upsell-data-id").val()
                                $.ajax({
                                    method: "POST",
                                    url: "/add-upsell-to-cart",
                                    data: {
                                        'product_id': product_id,
                                        'price': price,
                                        'image_url': image,
                                        'upsell_name': upsell_name,
                                        'upsell_id': upsell_id,
                                        csrfmiddlewaretoken: token,
                                    },
                                    success: function (response){
                                        $('.sidecart-inner').load(location.href + " .sidecart-inner");
                                        $('.checkout-form-inner').load(location.href + " .checkout-form-inner")
                                    }
                                })

                                
                            }
                        })


                    }
                
                if($(button).hasClass("proceed-to-checkout")){
                    $("#checkout_form_overlay").toggle();
                    $('body').toggleClass("checkout-is-active");
                    $.ajax({
                        method: "POST",
                        url: "/call-pixel-checkout",
                        data: {
                            csrfmiddlewaretoken: token,
                        },
                    })
                }    
                else
                {     
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
        $(".attribute-title").css("color", "red").animate({'font-size':'16px', 'font-weight':'700'}, 300).animate({'font-size':'12px', 'font-weight':'700'});
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
        var product_qty = $(this).closest('.offer-box').find('.qty-input').val();
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
        if($(this).hasClass('disabled')){
            return;
        }
        attrib_title = ': ' + $(this).find('.attrib_title').val();
     
        var attrib_id = $(this).find('.attrib_id').val();

        if($('.' + attrib_id + '_variable').length){
            image = $('.' + attrib_id + '_variable').not(".slick-cloned");
            $('.slider-holder').slick('slickGoTo', image.index() - 1);
        }
      
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
        console.log(product_id,product_qty,attribute_id,token)
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
                $('.sidecart-inner').load(location.href + " .sidecart-inner");
                $('.checkout-form-inner').load(location.href + " .checkout-form-inner");
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
                cartCount = cartCount - parseInt(cart_quantity)  
                $('.sidecart-inner').load(location.href + " .sidecart-inner")
                $('.checkout-form-inner').load(location.href + " .checkout-form-inner");
                $("#cart-count").html(cartCount)
                if($(".checkout-items-count").val() == 1){
                    console.log('yea')
                    if($('body').hasClass('checkout-is-active')){
                        $("#checkout_form_overlay").toggle();
                        $('body').toggleClass("checkout-is-active");
                    }
                }
                
                
            }
        })
    })
    

    $(document).on('click', '.fee-item', function(e){
        e.preventDefault();
        fee = $(this);
        fee_action = 'add';
        if($(this).hasClass('checked')){
            fee_action = 'remove';
        }
        var fee_id = $(this).find('.fee_data').val();
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
                $(fee).toggleClass('checked')
                $('.checkout-form-inner').load(location.href + " .checkout-form-inner");
                
            }
        })
        
    })
    

    $(".toggle-title").click(function (e){
        $(this).next(".toggle-content").slideToggle("fast");
    })
    $(".faq-title").click(function (e){
        $(this).next(".faq-content").slideToggle("fast");
        $(this).find(".faq-icon").toggleClass("vertical-flip");
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
        var min = 45,
          max = 60;
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
        setTimeout(myFunction, (Math.floor(Math.random() * (30 - 20 + 1) + 20)) * 1000)
    }
 })

 
function create_custom_dropdowns() {
    $('select').each(function (i, select) {
        if (!$(this).next().hasClass('dropdown-select')) {
            $(this).after('<div class="dropdown-select wide ' + ($(this).attr('class') || '') + '" tabindex="0"><span class="current"></span><div class="list"><ul></ul></div></div>');
            var dropdown = $(this).next();
            if(window.matchMedia("(max-width: 767px)").matches){
                $(dropdown).addClass('ismobile')
            }
            var options = $(select).find('option');
            var selected = $(this).find('option:selected');
            dropdown.find('.current').html(selected.data('display-text') || selected.text());
            options.each(function (j, o) {
                var display = $(o).data('display-text') || '';
                dropdown.find('ul').append('<li class="option ' + ($(o).is(':selected') ? 'selected' : '') + '" data-value="' + $(o).val() + '" data-display-text="' + display + '">' + $(o).text() + '<span style="display:none">' + $(o).attr("fake-name") + '</span></li>');
            });
        }
    });

    $('.dropdown-select ul').before('<div class="dd-search"><input id="txtSearchValue" autocomplete="off" onkeyup="filter()" class="dd-searchbox" type="text"></div>');
}

// Event listeners

// Open/close
$(document).on('click', '.dropdown-select', function (event) {
    $(this).removeClass('red')
    if($(event.target).hasClass('dd-searchbox')){
        return;
    }
    $('.dropdown-select').not($(this)).removeClass('open');
    $(this).toggleClass('open');
    if ($(this).hasClass('open')) {
        $(this).find('.option').attr('tabindex', 0);
        $(this).find('.selected').focus();
        $("#txtSearchValue").focus();
        if($(this).hasClass('ismobile')){
            $('html, body').animate({
                scrollTop: $(this).offset().top - 100
            }, 800);
        }
    } else {
        $(this).find('.option').removeAttr('tabindex');
        $(this).focus();
    }
});

// Close when clicking outside
$(document).on('click', function (event) {
    if ($(event.target).closest('.dropdown-select').length === 0) {
        $('.dropdown-select').removeClass('open');
        $('.dropdown-select .option').removeAttr('tabindex');
    }
    event.stopPropagation();
});

function filter(){
    var valThis = $('#txtSearchValue').val();
    $('.dropdown-select ul > li').each(function(){
     var text = $(this).text();
        (text.toLowerCase().indexOf(valThis.toLowerCase()) > -1) ? $(this).show() : $(this).hide();         
   });
};
// Search

// Option click
$(document).on('click', '.dropdown-select .option', function (event) {
    input = $(".checksout-city");
    $(this).closest('.list').find('.selected').removeClass('selected');
    $(this).addClass('selected');
    var text = $(this).data('value');
    $(this).closest('.dropdown-select').find('.current').text(text);
    $(this).closest('.dropdown-select').prev('select').val($(this).data('value')).trigger('change');
    $(input).val(text);
    
});

// Keyboard events
$(document).on('keydown', '.dropdown-select', function (event) {
    var focused_option = $($(this).find('.list .option:focus')[0] || $(this).find('.list .option.selected')[0]);
    // Space or Enter
    //if (event.keyCode == 32 || event.keyCode == 13) {
    if (event.keyCode == 13) {
        if ($(this).hasClass('open')) {
            focused_option.trigger('click');
        } else {
            $(this).trigger('click');
        }
        return false;
        // Down
    } else if (event.keyCode == 40) {
        if (!$(this).hasClass('open')) {
            $(this).trigger('click');
        } else {
            focused_option.next().focus();
        }
        return false;
        // Up
    } else if (event.keyCode == 38) {
        if (!$(this).hasClass('open')) {
            $(this).trigger('click');
        } else {
            var focused_option = $($(this).find('.list .option:focus')[0] || $(this).find('.list .option.selected')[0]);
            focused_option.prev().focus();
        }
        return false;
        // Esc
    } else if (event.keyCode == 27) {
        if ($(this).hasClass('open')) {
            $(this).trigger('click');
        }
        return false;
    }
});

$(document).ready(function () {
    create_custom_dropdowns();
    $(document).on('click', '#place_order', function (e){
        var city = $(".checksout-city").val();
        if(city === 'Undefined' || city === 'Одбери град'){
            e.preventDefault();
            $(".dropdown-select").addClass('red-city')
                $('#checkout_form_overlay').animate({
                    scrollTop: $(".dropdown-select").offset().top - 100
                }, 800);
            return;
        }
    })
    
    var token = $('input[name=csrfmiddlewaretoken]').val()
    ;(function($){
        $.fn.extend({
            donetyping: function(callback,timeout){
                timeout = timeout || 1e3; // 1 second default timeout
                var timeoutReference,
                    doneTyping = function(el){
                        if (!timeoutReference) return;
                        timeoutReference = null;
                        callback.call(el);
                    };
                return this.each(function(i,el){
                    var $el = $(el);

                    $el.is(':input') && $el.on('keyup keypress paste',function(e){

                        if (e.type=='keyup' && e.keyCode!=8) return;

                        if (timeoutReference) clearTimeout(timeoutReference);
                        timeoutReference = setTimeout(function(){
                            doneTyping(el);
                        }, timeout);
                    }).on('blur',function(){
                        doneTyping(el);
                    });
                });
            }
        });
    })(jQuery);
    $('#checkout_input_name').donetyping(function(){
      input_name = $('#checkout_input_name').val();
      input_phone = $('#checkout_input_phone').val()
      input_address = $('#checkout_input_address').val()
      $.ajax({
        method: "POST",
        url: "/check-abandoned-carts",
        data: {
            'name': input_name,
            'phone': input_phone,
            'address': input_address,
            csrfmiddlewaretoken: token,
        },
        success: function(response){
        }
      })
    }, 3000);
    $('#checkout_input_phone').donetyping(function(){
      input_name = $('#checkout_input_name').val();
      input_phone = $('#checkout_input_phone').val()
      input_address = $('#checkout_input_address').val()
      $.ajax({
        method: "POST",
        url: "/check-abandoned-carts",
        data: {
            'name': input_name,
            'phone': input_phone,
            'address': input_address,
            csrfmiddlewaretoken: token,
        },
        success: function(response){
        }
      })
      }, 3000);
    $('#checkout_input_address').donetyping(function(){
        input_name = $('#checkout_input_name').val();
        input_phone = $('#checkout_input_phone').val()
        input_address = $('#checkout_input_address').val()
        $.ajax({
          method: "POST",
          url: "/check-abandoned-carts",
          data: {
              'name': input_name,
              'phone': input_phone,
              'address': input_address,
              csrfmiddlewaretoken: token,
          },
          success: function(response){
          }
        })
        }, 3000);
    $(document).on("click", ".product-page-upsell", function(){
        current_item = $(this)
        $(this).toggleClass("checked");
        $(this).find(".product-upsell-checkbox").toggleClass("checked");

        $(".product-page-upsell").each(function(i, obj){
            if($(this).hasClass("checked")){
                var upsell_name = $(this).find(".product-upsell-title-data").val();
                console.log(upsell_name)
            }
        })
        var image = $(this).find(".product-upsell-image").attr('src')
        var price = $(this).find(".product-upsell-price-data").val();
        var product_id = $("#main-product-id").val();
        var upsell_name = $(this).find(".product-upsell-title-data").val();
        $.ajax({
            method: "POST",
            url: "/upsell-add-to-cart",
            data: {
                'product_id': product_id,
                'upsell_title': upsell_name,
                'upsell_price': price,
                'thumbnail_url': image,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                console.log(response)

            }
        })
        

    });
    $(document).on("click", ".sidecartCheckout", function(e){
        $("#checkout_form_overlay").toggle();
        $('body').toggleClass("checkout-is-active");
        $.ajax({
            method: "POST",
            url: "/call-pixel-checkout",
            data: {
                csrfmiddlewaretoken: token,
            },
        })
    })
    $(document).on("click", "#close-checkout", function(e){
        e.preventDefault();
        if($('body').hasClass('checkout-is-active')){
            $("#checkout_form_overlay").toggle();
            $('body').toggleClass("checkout-is-active");
        }
    })
    $(document).on("click", ".product-page-upsell", function(){
        current_item = $(this)
        $(this).toggleClass("checked");
        $(this).find(".product-upsell-checkbox").toggleClass("checked");

    });
});




