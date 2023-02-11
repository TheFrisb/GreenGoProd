
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
    input = $(".checkout-city");
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
        var city = $(".checkout-city").val();
        if(city === 'Undefined' || city === 'Одбери град'){
            e.preventDefault();
            $(".dropdown-select").addClass('red')
                $('html, body').animate({
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
    
});




