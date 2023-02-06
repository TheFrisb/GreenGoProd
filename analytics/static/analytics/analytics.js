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
                row.html(comment);
                $('.alert').fadeToggle();
                $('.alert').delay(5000).fadeToggle();

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
    
});
