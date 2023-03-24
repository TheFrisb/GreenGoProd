function create_custom_dropdowns(){$("select").each(function(t,e){if(!$(this).next().hasClass("dropdown-select")){$(this).after('<div class="dropdown-select wide '+($(this).attr("class")||"")+'" tabindex="0"><span class="current"></span><div class="list"><ul></ul></div></div>');var a=$(this).next();window.matchMedia("(max-width: 767px)").matches&&$(a).addClass("ismobile");var i=$(e).find("option"),c=$(this).find("option:selected");a.find(".current").html(c.data("display-text")||c.text()),i.each(function(t,e){var i=$(e).data("display-text")||"";a.find("ul").append('<li class="option '+($(e).is(":selected")?"selected":"")+'" data-value="'+$(e).val()+'" data-display-text="'+i+'">'+$(e).text()+'<span style="display:none">'+$(e).attr("fake-name")+"</span></li>")})}}),$(".dropdown-select ul").before('<div class="dd-search"><input id="txtSearchValue" autocomplete="off" onkeyup="filter()" class="dd-searchbox" type="text"></div>')}function filter(){var t=$("#txtSearchValue").val();$(".dropdown-select ul > li").each(function(){$(this).text().toLowerCase().indexOf(t.toLowerCase())>-1?$(this).show():$(this).hide()})}$(document).ready(function(){let t=parseInt($(".main-price").find(".product-regular-price").text()),e=parseInt($(".main-price").find(".product-sale-price").text()),a=$(".main-price").find(".money_saved").text(),i=$(".main-price").find(".percentage").text(),c=$(".product-attributes").find(".attribute-title").text();var s=parseInt($("#cart-count").text());function o(){$("#sidecart").toggleClass("sidecart-active"),$(".lightbox").toggleClass("lightbox-active")}function r(){$(".lightbox").toggleClass("lightbox-active lightbox-search"),$(".lightbox").find("form").toggleClass("disabled")}$("div#container").on("click","button.alert",function(){alert(1)}),$(".header-menu").click(function(t){$(this).toggleClass("active"),$("#navigation").toggleClass("active")}),$("#search-mobile").click(function(t){r()}),$(".close-search").click(function(t){r()}),$(".header-cart").click(function(t){!1==$("#sidecart").hasClass("sidecart-active")&&o()}),$(".cart-close").click(function(t){o()}),$(".lightbox").click(function(){$("#sidecart").hasClass("sidecart-active")&&o()}),slide1=$(".slider-wrapper1").find(".slide").innerWidth(),slide2=$(".slider-wrapper2").find(".slide").innerWidth();var d=1,n=1,l=$(".slider-wrapper1").find(".slide").length,u=$(".slider-wrapper2").find(".slide").length;function f(){var t=Math.floor(57*Math.random()+1);let e=["Александар","Ангела","Марија","Елена","Здравко","Зорица","Костадин","Живка","Никола","Ева","Наум","Филип","Бранкица","Мартин","Ивана","Ристе","Лилјана","Борис","Ефимија","Живко","Христина","Васил"];var a=e[Math.floor(Math.random()*e.length)];$.ajax({url:"/get_recent_ordered",type:"GET",dataType:"json",success:function(e){$("#ordered_items_notice").attr("href",e.url),$("#ordered_product_thumbnail").attr("src",e.thumbnail),$("#order_person_name").html(a),$("#order_person_product_name").html(e.title),$("#order_product_regular_price").html(e.regular_price),$("#order_product_sale_price").html(e.sale_price),$("#ordered_items_notice_wrapper").fadeToggle(400),$("#order_time_minutes_ago").html(t),setTimeout(function(){$("#ordered_items_notice_wrapper").fadeOut(400)},5e3)}}),setTimeout(f,1e3*Math.floor(16*Math.random()+45))}$(".slider-wrapper1").on("click",".slide-arrow",function(){slidescontainer=$(".slide-arrow-next1").next("ul"),$(this).hasClass("slide-arrow-next1")&&(slidescontainer.scrollLeft(slide1*d),(slide1>220&&d<l-3||slide1<220&&d<l-1)&&d++),$(this).hasClass("slide-arrow-prev1")&&(slideleft=slide1*(d-1),slidescontainer.scrollLeft(slideleft-slide1),d>1&&d--)}),$(".slider-wrapper2").on("click",".slide-arrow",function(){slidescontainer=$(".slide-arrow-next2").next("ul"),$(this).hasClass("slide-arrow-next2")&&(slidescontainer.scrollLeft(slide2*n),(slide2>220&&n<u-3||slide2<220&&n<u-1)&&n++),$(this).hasClass("slide-arrow-prev2")&&(slideleft=slide2*(n-1),slidescontainer.scrollLeft(slideleft-slide2),n>1&&n--)}),$(document).on("click",".increment-btn",function(t){t.preventDefault();var e=$(this).closest(".product_data").find(".qty-input").val(),a=parseInt(e,10);a=isNaN(a)?0:a,a++,$(this).closest(".product_data").find(".qty-input").val(a)}),$(document).on("click",".decrement-btn",function(t){t.preventDefault();var e=$(this).closest(".product_data").find(".qty-input").val(),a=parseInt(e,10);(a=isNaN(a)?0:a)>1&&(a--,$(this).closest(".product_data").find(".qty-input").val(a))}),$(document).on("click",".add-to-cartBtn",function(t){button=$(this),t.stopPropagation(),t.preventDefault(),$(this).find(".load-spinner").css("display","inline-block"),$(this).find(".btn-text").css("display","none");var e=$(this).closest(".product_data").find(".prod_id").val(),a=$(this).closest(".product_data").find(".qty-input").val();$(this).closest(".product_data").find(".product-price-tracker").text(),$(this.closest(".product_data")).find(".prod_title_tracker").text();var i=$("input[name=csrfmiddlewaretoken]").val();if(null==a&&(a=1),$(button).hasClass("stickyBtn")){var e=$(".product-page.product_data").find(".prod_id").val(),a=$(".product-page.product_data").find(".qty-input").val();null==a&&(a=1)}$.ajax({method:"POST",url:"/add-to-cart",data:{product_id:e,product_qty:a,csrfmiddlewaretoken:i},success:function(t){$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner"),s++,$("#cart-count").html(s),$(button).hasClass("hasUpsells")&&(console.log("called 1"),$(".product-page-upsell").each(function(t,e){if($(this).hasClass("checked")){var a=$(this).find(".product-upsell-image").attr("src"),c=$(this).find(".product-upsell-price-data").val(),s=$(this).find(".product-upsell-product-id").val(),o=$(this).find(".product-upsell-title-data").val(),r=$(this).find(".product-upsell-data-id").val();$.ajax({method:"POST",url:"/add-upsell-to-cart",data:{product_id:s,price:c,image_url:a,upsell_name:o,upsell_id:r,csrfmiddlewaretoken:i},success:function(t){$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner")}})}})),$(button).hasClass("sidecartOfferBtn")?!1==$(button).hasClass("addedBtn")?$(button).toggleClass("addedBtn").html("ДОДАДЕН"):o():$(button).hasClass("proceed-to-checkout")?($("#checkout_form_overlay").toggle(),$("body").toggleClass("checkout-is-active"),$.ajax({method:"POST",url:"/call-pixel-checkout",data:{csrfmiddlewaretoken:i}})):!1==$(button).hasClass("mainaddedBtn")?setTimeout(()=>{$(button).toggleClass("mainaddedBtn").html("ДОДАДЕН"),o()},250):o()}})}),$(document).on("click",".offerBtn",function(t){if(t.stopPropagation(),t.preventDefault(),button=$(this),!$(button).hasClass("addedBtn")){var e=$(this).closest(".product_data").find(".prod_id").val(),a=1,i=$(this).closest(".product_data").find(".offer_price").val();if($(this).hasClass("checkout-offer")){var e=$(this).siblings(".prod_id").val(),a=1,i=$(this).siblings(".offer_price").val();console.log(e,i)}$(this.closest(".product_data")).find(".prod_title_tracker").text();var c=$("input[name=csrfmiddlewaretoken]").val();null==a&&(a=1),$.ajax({method:"POST",url:"/offer-add-to-cart",data:{product_id:e,product_qty:a,product_price:i,csrfmiddlewaretoken:c},success:function(t){s++,$("#cart-count").html(s),$(button).hasClass("sidecartOfferBtn")?!1==$(button).hasClass("addedBtn")&&$(button).toggleClass("addedBtn").html("ДОДАДЕН"):$(button).hasClass("add-upsell")&&!1==$(button).hasClass("addedBtn")&&$(button).toggleClass("addedBtn").html("ДОДАДЕН"),$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner")}})}}),$(document).on("click",".variable-add-to-cartBtn",function(t){button=$(this);var e=$(this).closest(".product_data").find(".prod_id").val(),a=$(this).closest(".product_data").find(".qty-input").val(),i=$(".product-attributes").find(".attribute-item.active");$(this.closest(".product_data")).find(".prod_title_tracker").text();var c=$("input[name=csrfmiddlewaretoken]").val(),r=0,d=null;if(null==a&&(a=1),$(button).hasClass("stickyBtn")){var e=$(".product-page.product_data").find(".prod_id").val(),a=$(".product-page.product_data").find(".qty-input").val();null==a&&(a=1)}$(i).length?(r=$(i).find(".attrib_id").val(),d=$(i).find(".attrib_type").val(),product_price=$(".main-price").find(".product-price-tracker").text(),$(this).find(".load-spinner").css("display","inline-block"),$(this).find(".btn-text").css("display","none"),$.ajax({method:"POST",url:"/variable-add-to-cart",data:{product_id:e,product_qty:a,attribute_id:r,csrfmiddlewaretoken:c},success:function(t){s+=parseInt(a),$("#cart-count").html(s),$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner"),$(button).hasClass("hasUpsells")&&(console.log("called 1"),$(".product-page-upsell").each(function(t,e){if($(this).hasClass("checked")){var a=$(this).find(".product-upsell-image").attr("src"),i=$(this).find(".product-upsell-price-data").val(),s=$(this).find(".product-upsell-product-id").val(),o=$(this).find(".product-upsell-title-data").val(),r=$(this).find(".product-upsell-data-id").val();$.ajax({method:"POST",url:"/add-upsell-to-cart",data:{product_id:s,price:i,image_url:a,upsell_name:o,upsell_id:r,csrfmiddlewaretoken:c},success:function(t){$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner")}})}})),$(button).hasClass("proceed-to-checkout")?($("#checkout_form_overlay").toggle(),$("body").toggleClass("checkout-is-active"),$.ajax({method:"POST",url:"/call-pixel-checkout",data:{csrfmiddlewaretoken:c}})):!1==$(button).hasClass("mainaddedBtn")?setTimeout(()=>{$(button).toggleClass("mainaddedBtn").html("ДОДАДЕН"),o()},250):o()}})):$(".attribute-title").css("color","red").animate({"font-size":"16px","font-weight":"700"},300).animate({"font-size":"12px","font-weight":"700"})}),$(".offer-box").on("click",".offer-button",function(t){if(button=$(this),$(button).hasClass("addedBtn"))return 1;t.stopPropagation(),t.preventDefault();var e=$(this).closest(".offer-box").find(".order_id").val(),a=$(this).closest(".offer-box").find(".prod_id").val(),i=$(this).closest(".offer-box").find(".qty-input").val(),c=$("input[name=csrfmiddlewaretoken]").val();$.ajax({method:"POST",url:"/add-to-order",data:{order_id:e,product_id:a,product_qty:i,csrfmiddlewaretoken:c},success:function(t){$(button).addClass("addedBtn").html("ДОДАДЕН"),$(".cart-data").load(location.href+" .cart-data")}})}),$(".sidecart-offer-item").on("click","sidecart-offer-item",function(t){t.preventDefault()}),$(".product-attributes").on("click",".attribute-item",function(){if(!$(this).hasClass("disabled")){attrib_title=": "+$(this).find(".attrib_title").val();var s=$(this).find(".attrib_id").val();$("."+s+"_variable").length&&(image=$("."+s+"_variable").not(".slick-cloned"),$(".slider-holder").slick("slickGoTo",image.index()-1)),$(this).hasClass("offer")?(offer_regular_price=t*$(this).index(),offer_price=parseInt($(this).find(".offer-price").text()),$(".main-price").find(".product-regular-price").text(offer_regular_price+" ден"),$(".main-price").find(".product-price-tracker").text(offer_price),1!=$(this).index()?($(".main-price").find(".money_saved").text(parseInt(offer_regular_price-offer_price)),$(".main-price").find(".percentage").text("-"+parseInt(100-offer_price/offer_regular_price*100)+"%")):($(".main-price").find(".money_saved").text(a),$(".main-price").find(".percentage").text(i))):(offer_price=$(this).find(".attrib_price").val(),e!=offer_price?(offer_regular_price=t*$(this).index(),$(".main-price").find(".product-regular-price").text(offer_regular_price+" ден"),$(".main-price").find(".money_saved").text(parseInt(offer_regular_price-offer_price)),$(".main-price").find(".percentage").text("-"+parseInt(100-offer_price/offer_regular_price*100)+"%")):(offer_regular_price=t,$(".main-price").find(".product-regular-price").text(offer_regular_price+" ден"),$(".main-price").find(".money_saved").text(a),$(".main-price").find(".percentage").text(i)),$(".main-price").find(".product-price-tracker").text(offer_price)),$(".product-attributes div").removeClass("active"),$(this).toggleClass("active"),$(".attribute-title").text(c+attrib_title),$(".attribute-title").css("color","#0f0f0f")}}),$(document).on("click",".changeQuantity",function(t){t.preventDefault(),button=$(this);var e=$(this).closest(".product_data").find(".prod_id").val(),a=$(this).closest(".product_data").find(".qty-input").val(),i=0;$(this).closest(".product_data").find(".attrib_id").val()>0&&(i=$(this).closest(".product_data").find(".attrib_id").val());var c=$("input[name=csrfmiddlewaretoken]").val();console.log(e,a,i,c),$.ajax({method:"POST",url:"/update-cart",data:{product_id:e,product_qty:a,attribute_id:i,csrfmiddlewaretoken:c},success:function(t){$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner")}})}),$(document).on("click",".remove-item",function(t){t.preventDefault();var e=$(this).closest(".product_data").find(".prod_id").val(),a=parseInt($(this).closest(".product_data").find(".sidecart-item-quantity").text()),i=0;$(this).closest(".product_data").find(".attrib_id").val()>0&&(i=$(this).closest(".product_data").find(".attrib_id").val());var c=$("input[name=csrfmiddlewaretoken]").val();$("#cart_items_count").val(),$.ajax({method:"POST",url:"/delete-cart-item",data:{product_id:e,attribute_id:i,csrfmiddlewaretoken:c},success:function(t){s-=parseInt(a),$(".sidecart-inner").load(location.href+" .sidecart-inner"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner"),$("#cart-count").html(s),1==$(".checkout-items-count").val()&&(console.log("yea"),$("body").hasClass("checkout-is-active")&&($("#checkout_form_overlay").toggle(),$("body").toggleClass("checkout-is-active")))}})}),$(document).on("click",".fee-item",function(t){t.preventDefault(),fee=$(this),fee_action="add",$(this).hasClass("checked")&&(fee_action="remove");var e=$(this).find(".fee_data").val(),a=$("input[name=csrfmiddlewaretoken]").val();$.ajax({method:"POST",url:"/add-or-delete-fee",data:{fee_id:e,action:fee_action,csrfmiddlewaretoken:a},success:function(t){$(fee).toggleClass("checked"),$(".checkout-form-inner").load(location.href+" .checkout-form-inner")}})}),$(".toggle-title").click(function(t){$(this).next(".toggle-content").slideToggle("fast")}),$(".faq-title").click(function(t){$(this).next(".faq-content").slideToggle("fast"),$(this).find(".faq-icon").toggleClass("vertical-flip")}),$(".checkout-dostava").click(function(t){$(".checkout-garancija").hasClass("active")&&($(".checkout-garancija").removeClass("active"),$(".checkout-garancija-content").slideToggle("fast")),$(this).toggleClass("active"),$(".checkout-dostava-content").slideToggle("fast")}),$(".checkout-garancija").click(function(t){$(".checkout-dostava").hasClass("active")&&($(".checkout-dostava").removeClass("active"),$(".checkout-dostava-content").slideToggle("fast")),$(this).toggleClass("active"),$(".checkout-garancija-content").slideToggle("fast")}),$("#ordered_items_notice_wrapper")&&($(document).on("click","#close_ordered_items_notice",function(t){t.preventDefault(),$("#ordered_items_notice_wrapper").fadeOut(200)}),setTimeout(f,1e3*Math.floor(11*Math.random()+20)))}),$(document).on("click",".dropdown-select",function(t){$(this).removeClass("red"),!$(t.target).hasClass("dd-searchbox")&&($(".dropdown-select").not($(this)).removeClass("open"),$(this).toggleClass("open"),$(this).hasClass("open")?($(this).find(".option").attr("tabindex",0),$(this).find(".selected").focus(),$("#txtSearchValue").focus(),$(this).hasClass("ismobile")&&$("html, body").animate({scrollTop:$(this).offset().top-100},800)):($(this).find(".option").removeAttr("tabindex"),$(this).focus()))}),$(document).on("click",function(t){0===$(t.target).closest(".dropdown-select").length&&($(".dropdown-select").removeClass("open"),$(".dropdown-select .option").removeAttr("tabindex")),t.stopPropagation()}),$(document).on("click",".dropdown-select .option",function(t){input=$(".checksout-city"),$(this).closest(".list").find(".selected").removeClass("selected"),$(this).addClass("selected");var e=$(this).data("value");$(this).closest(".dropdown-select").find(".current").text(e),$(this).closest(".dropdown-select").prev("select").val($(this).data("value")).trigger("change"),$(input).val(e)}),$(document).on("keydown",".dropdown-select",function(t){var e=$($(this).find(".list .option:focus")[0]||$(this).find(".list .option.selected")[0]);if(13==t.keyCode)return $(this).hasClass("open")?e.trigger("click"):$(this).trigger("click"),!1;if(40==t.keyCode)return $(this).hasClass("open")?e.next().focus():$(this).trigger("click"),!1;if(38==t.keyCode){if($(this).hasClass("open")){var e=$($(this).find(".list .option:focus")[0]||$(this).find(".list .option.selected")[0]);e.prev().focus()}else $(this).trigger("click");return!1}if(27==t.keyCode)return $(this).hasClass("open")&&$(this).trigger("click"),!1}),$(document).ready(function(){create_custom_dropdowns(),$(document).on("click","#place_order",function(t){var e=$(".checksout-city").val();if("Undefined"===e||"Одбери град"===e){t.preventDefault(),$(".dropdown-select").addClass("red-city"),$("#checkout_form_overlay").animate({scrollTop:$(".dropdown-select").offset().top-100},800);return}});var t=$("input[name=csrfmiddlewaretoken]").val();(function(t){t.fn.extend({donetyping:function(e,a){a=a||1e3;var i,c=function(t){i&&(i=null,e.call(t))};return this.each(function(e,s){var o=t(s);o.is(":input")&&o.on("keyup keypress paste",function(t){("keyup"!=t.type||8==t.keyCode)&&(i&&clearTimeout(i),i=setTimeout(function(){c(s)},a))}).on("blur",function(){c(s)})})}})})(jQuery),$("#checkout_input_name").donetyping(function(){input_name=$("#checkout_input_name").val(),input_phone=$("#checkout_input_phone").val(),input_address=$("#checkout_input_address").val(),$.ajax({method:"POST",url:"/check-abandoned-carts",data:{name:input_name,phone:input_phone,address:input_address,csrfmiddlewaretoken:t},success:function(t){}})},3e3),$("#checkout_input_phone").donetyping(function(){input_name=$("#checkout_input_name").val(),input_phone=$("#checkout_input_phone").val(),input_address=$("#checkout_input_address").val(),$.ajax({method:"POST",url:"/check-abandoned-carts",data:{name:input_name,phone:input_phone,address:input_address,csrfmiddlewaretoken:t},success:function(t){}})},3e3),$("#checkout_input_address").donetyping(function(){input_name=$("#checkout_input_name").val(),input_phone=$("#checkout_input_phone").val(),input_address=$("#checkout_input_address").val(),$.ajax({method:"POST",url:"/check-abandoned-carts",data:{name:input_name,phone:input_phone,address:input_address,csrfmiddlewaretoken:t},success:function(t){}})},3e3),$(document).on("click",".sidecartCheckout",function(e){$("#checkout_form_overlay").toggle(),$("body").toggleClass("checkout-is-active"),$.ajax({method:"POST",url:"/call-pixel-checkout",data:{csrfmiddlewaretoken:t}})}),$(document).on("click","#close-checkout",function(t){t.preventDefault(),$("body").hasClass("checkout-is-active")&&($("#checkout_form_overlay").toggle(),$("body").toggleClass("checkout-is-active"))}),$(document).on("click",".product-page-upsell",function(){!(current_item=$(this)).hasClass("free-upsell")&&($(this).toggleClass("checked"),$(this).find(".product-upsell-checkbox").toggleClass("checked"))})});
