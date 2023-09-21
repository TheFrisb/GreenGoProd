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
                dropdown.find('ul').append('<li class="option ' + ($(o).is(':selected') ? 'selected' : '') + '" data-value="' + $(o).val() + '"data-url="'+ $(o).attr("data-url") + '" data-display-text="' + display + '">' + $(o).text() + '<span style="display:none">' + $(o).attr("fake-name")  + '</span></li>');
            });
        }
    });

    $('.dropdown-select ul').before('<div class="dd-search"><input id="txtSearchValue" autocomplete="off" onkeyup="filter()" class="dd-searchbox" type="text"></div>');
}

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
    var id = 0;
    var token = $('input[name=csrfmiddlewaretoken]').val()
    var row = null;
    create_custom_dropdowns();
    $(document).on('click', '#change_product',function (e){
        e.preventDefault();
        url = $(".dropdown-select").find(".selected").attr("data-url");
        console.log(url);
        window.location.href = url;
    })
    $(document).on('click', '.add_comment_button', function (e){
        e.preventDefault();
        id = $(this).attr("data-row-id");
        $('#addCommentModal').modal('show');
        row = $(this).closest("td");
    })
    $(document).on('click', '.close-modal', function (e){
        $('#addCommentModal').modal('hide');
        
    })
    $(document).on('click', '#submit_comment', function(e){
        comment = $('#enter_comment').val();
        console.log(id);
        console.log(comment);
        $.ajax({
            method: "POST",
            url: "/analytics/add_comment",
            data: {
                'comment': comment,
                'id': id,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                $('#addCommentModal').modal('hide');
                let remove_comment_btn = `<button class="btn btn-outline-danger btn-sm delete_comment_button" data-row-id="${id}" >ОТСТРАНИ</button>`;
                row.html(comment);
                row.append("<br>")
                row.append(remove_comment_btn);
                $('.alert').fadeToggle();
                $('.alert').delay(5000).fadeToggle();

            }
        })
    })

    $(document).on('click', '.delete_comment_button', function(e){
        let button = $(this);
        let current_row = button.closest('td');
        let row_id = button.data('row-id');
        $.ajax({
            method: "POST",
            url: "/analytics/delete-comment",
            data: {
                'id': row_id,
                csrfmiddlewaretoken: token,
            },

            success: function (response){
                let add_comment_btn = `<button class="btn btn-outline-primary btn-sm add_comment_button" data-row-id="${row_id}" >ДОДАДИ</button>`;
                current_row.html(add_comment_btn);
            }
        })
    })


    $(document).on('click', '#enter_old_row', function(e){
        e.preventDefault();
        owner = $('#owner').val();
        var old_row_ad_spend = $('#old_row_ad_spend').val()
        old_row_date = $('#old_row_date').val();
        var total_quantity = $('#old_row_quantity').val()
        console.log(owner, old_row_ad_spend, old_row_date, total_quantity)
        $.ajax({
            method: "POST",
            url: "/analytics/add_old_row",
            data: {
                'owner': owner,
                'ad_spend': old_row_ad_spend,
                'date': old_row_date,
                'quantity': total_quantity,
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                $('#table').load(location.href + " #table")
                console.log('Successfully added old row!')
            }
        })
    })
    $("#campaign-list").bind('mousewheel', function(e) {
        e.preventDefault()
        if ($("#campaign-list").is(":hover")) {
         if (e.originalEvent.wheelDelta / 120 > 0) {
           $(this).scrollLeft($(this).scrollLeft() - 100);
         }
         else {
          $(this).scrollLeft($(this).scrollLeft() + 100);
         }
        }
       });
    current_item = $("#current_item").text();
    list_items = $("#campaign-list a")
    for(let i = 0; i < list_items.length; i++){
        text = $(list_items[i]).text();
        if(current_item == text){
            scroll_to_index = $(list_items[i]).index()
            $("#campaign-list").scrollLeft(500 * scroll_to_index)
        }
    }
    
    $(document).on('click', '#get_dated_ad_spend', function(e){
        e.preventDefault();
        var date = $("#ad_spend_datepicker").val()
        $.ajax({
            method: "GET",
            url: "/analytics/get_ad_spend_by_date",
            data: {
                'date': date,
                csrfmiddlewaretoken: token,
            },

            success: function(response){

                $("#retrieved_ad_spend").text(response['ad_spend'] + ' мкд')
            }
        })
    })
    
        $(document).on("click", "#adspend_retriever", function(e){
        e.preventDefault();
        var date_from = $("#datepicker_from").val();
        var date_till = $("#datepicker_till").val();
        if(date_till.length == 0){
            date_till = date_from
        }
    
        var button = $(this);

        $.ajax({
            method: "GET",
            url: "/analytics/retrieve_adspend",
            data: {
                'date_from': date_from,
                'date_till': date_till,
                csrfmiddlewaretoken: token,
            },
            success: function (response){
                $("#retrieved_adspend").show()
                $("#adspend_inUSD").text(response['USD_Val'])
                $.ajax({
                    method: "GET",
                    url: "https://v6.exchangerate-api.com/v6/8762058d6b172b396d60ffda/latest/USD",

                    success: function(exchange_response) {
                        var mkd_val = (response['USD_Val'] * exchange_response.conversion_rates.MKD).toFixed(2);
                        console.log(response['USD_Val'] * exchange_response.conversion_rates.MKD)
                        $("#adspend_inMKD").text(mkd_val);
                    }
                })

            }
        })
    })
});
