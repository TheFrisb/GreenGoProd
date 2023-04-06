function create_custom_dropdowns() {
    $('select:not(.form-select)').each(function (i, select) {
        if (!$(this).next().hasClass('dropdown-select')) {
            $(this).after('<div class="dropdown-select wide ' + ($(this).attr('class') || '') + '" tabindex="0"><span class="current" id="currently_selected_product"></span><div class="list"><ul></ul></div></div>');
            var dropdown = $(this).next();
            if(window.matchMedia("(max-width: 767px)").matches){
                $(dropdown).addClass('ismobile')
            }
            var options = $(select).find('option');
            var selected = $(this).find('option:selected');
            dropdown.find('.current').html(selected.data('display-text') || selected.text());
            options.each(function (j, o) {
                var display = $(o).data('display-text') || '';
                dropdown.find('ul').append('<li class="option ' + ($(o).is(':selected') ? 'selected' : '') + '" data-value="' + $(o).val() + '"data-id="'+ $(o).attr("data-id") + '" data-display-text="' + display + '">' + $(o).text() + '<span style="display:none">' + $(o).attr("fake-name")  + '</span></li>');
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
    input = $("#chosen_product");
    $(this).closest('.list').find('.selected').removeClass('selected');
    $(this).addClass('selected');
    var text = $(this).data('id');
    $(this).closest('.dropdown-select').find('.current').text(text);
    $(this).closest('.dropdown-select').prev('select').val($(this).data('value')).trigger('change');
    $(input).val(text);
    console.log('option selected')


    
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
    $.ajax({
        url: 'https://greengoshop.mk/analytics/get-open-audience',
        method: 'GET',
        data: {
            'csrfmiddlewaretoken': token
        },
        success: function (data) {
            // loop over all audience-select-value elements and append options from data
            var audience = data.audience;

            $(".dropdown-menu").each(function(index, element){
                $(element).append('<li class="dropdown-item"><input type="hidden" name="aud_id" class="audience_id" value="OPEN_AUDIENCE">' + '<input type="hidden" name="aud_name" class="audience_name" value="OPEN_AUDIENCE">' + audience.adset_name + '</li>')

            })
            
        }
    })
    
    
    var adset_count = 1;
    var token = $('input[name=csrfmiddlewaretoken]').val()
    create_custom_dropdowns();
    $('[data-toggle="tooltip"]').tooltip()

    var ad_template = $("#ad_template").clone();

    $(document).on('click', ".add_adset", function(e){
        e.preventDefault(e);
        adset_count += 1;
        var button = $(this);
        // the below doesnt work on appended elements
        var adset_template = $(button).closest('.adset_template').clone();
        $("#main_form").append(adset_template.clone());
        var primary_text = $(button).closest('.ad').find('.ad_primary_text').val()
        var headline = $(button).closest('.ad').find('.ad_headline').val()
        var description = $(button).closest('.ad').find('.ad_description').val()
        $(button).closest(".ad").after(ad_template.clone());
        if($(button).siblings('.checkbox-place').find('.ad_text_copied_checkbox').is(':checked')){
            $(button).closest(".ad").next('.ad').find('.ad_primary_text').val(primary_text)
            $(button).closest(".ad").next('.ad').find('.ad_headline').val(headline)
            $(button).closest(".ad").next('.ad').find('.ad_description').val(description)
        }



        $(button).closest(".adset_template").next().find(".adset_name").text("ADSET " + adset_count)

        // get new adset
        var new_adset = $(button).closest(".adset_template").next()
        $(new_adset).find('.adset_name_input').val("")
        $(new_adset).find('.chosen_ad_audience').val("");
        $(new_adset).find('.search_audience_input').val("");

        button.remove()
       
        
    })
    $(document).on('click', ".remove_adset", function(e){  
        e.preventDefault(e);
        // return if it's the only adset
        if(adset_count == 1){
            return;
        }

        var button = $(this);
        adset_count -= 1;
        $(button).closest(".adset_template").remove();
        // update count on all adsets
        $(".adset_name").each(function(index, value){
            $(value).text("ADSET " + (index + 1))
        })
        console.log(adset_count)
        if(adset_count==1){
            $(".adset_template").find($(".adset-button-holder")).prepend('<button class="btn btn-primary my-2 add_adset" id="add_adset">Додади нов Ad Set</button>')
        }
    })


    $(document).on('click', ".add_ad", function(e){
        e.preventDefault(e);
        var button = $(this);
        var primary_text = $(button).closest('.ad').find('.ad_primary_text').val()
        var headline = $(button).closest('.ad').find('.ad_headline').val()
        var description = $(button).closest('.ad').find('.ad_description').val()
        var current_ad_template = $(button).closest('.ad').clone();
        var parent_adset = $(button).closest('.adset_template')
        
        $(button).closest(".ad").after(current_ad_template.clone());
        if($(button).siblings('.checkbox-place').find('.ad_text_copied_checkbox').is(':checked')){
            $(button).closest(".ad").next('.ad').find('.ad_primary_text').val(primary_text)
            $(button).closest(".ad").next('.ad').find('.ad_headline').val(headline)
            $(button).closest(".ad").next('.ad').find('.ad_description').val(description)
        }

        $(button).remove();
        parent_adset.find(".ad").each(function(index, value){
            $(value).find(".ad_name").text("РЕКЛАМА " + (index + 1))
        })
        
    })
    $(document).on('click', ".remove_ad", function(e){
        e.preventDefault(e);
        var button = $(this);
        var parent_adset = $(button).closest('.adset_template')
        var first_ad = parent_adset.find(".ad").first()
        var ad_count = parent_adset.find(".ad").length
        // return if it's the only ad
        if(ad_count == 1){
            return;
        }
        ad_count -= 1;
        
        $(button).closest(".ad").remove();
        parent_adset.find(".ad").each(function(index, value){
            $(value).find(".ad_name").text("РЕКЛАМА " + (index + 1))
        })
        if(ad_count==1){
            $(first_ad).find($(".ad-button-holder .checkbox-place")).after('<button class="btn btn-primary btn-sm my-2 add_ad" type="Button">Додади нов AD</button>')
        }
    })

    $(document).on('click', '.dropdown-select .option', function (event) {
        
        var product_id = $(this).attr('data-id')
        $.ajax({
            url: 'https://greengoshop.mk/analytics/get-product',
            method: 'GET',
            data: {
                'product_id': product_id,
                'csrfmiddlewaretoken': token
            },
            success: function (data) {
                $("#product-card-image").attr("src", data.thumbnail)
                $("#product-card-title").text(data.title)
                $("#product-card-before-price").text(data.regular_price)
                $("#product-card-price").text(data.sale_price)
                $("#product_card_label").text(data.label)
                $("#product-card-link").attr("href", data.url)
                $("#product_card").show()
                $("#campaign_name").val('(mkd) ' + data.label)
            }
        })
    });

    $(document).on('click', '.select_ad_media_type_btn', function(e){
        if($(this).hasClass('media_type_photo')){
            $(this).closest(".ad_media_selector").siblings(".ad_media_photo").show();
            $(this).closest(".ad_media_selector").siblings(".ad_media_video").hide();
            if($(this).hasClass('btn-success')){
                return;
            }
            else{
                $(this).siblings('.media_type_video').removeClass('btn-success')
                $(this).addClass('btn-success')
            }
        }
        else if($(this).hasClass('media_type_video')){
            $(this).closest(".ad_media_selector").siblings(".ad_media_photo").hide();
            $(this).closest(".ad_media_selector").siblings(".ad_media_video").show();
            if($(this).hasClass('btn-success')){
                return;
            }
            else{
                $(this).siblings('.media_type_photo').removeClass('btn-success')
                $(this).addClass('btn-success')
            }
        }

    })

    $(document).on('click', '.submit_media_photo', function(e){
        e.preventDefault(e);
        var button = $(this);
        var file = $(button).siblings(".media_input_photo").prop('files')[0];
        if(file == null){
            $("#error_alert").text("Не си одберал/а слика, или сликата е лош формат(дозволени се само: .jpg, .png, .jpeg)");
            $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
            $(button).siblings(".media_input_photo").focus();
        }
        else{
            var data = new FormData();
            data.append('ad_image', file);
            data.append('csrfmiddlewaretoken', token);
            $.ajax({
                url: 'https://greengoshop.mk/analytics/upload-campaign-photo',
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data.image_url)
                    $(button).closest('.media_input').siblings('.media_holder').find('.media_preview').attr('src', data.image_url)
                    $(button).closest('.media_input').siblings('.media_holder').show();
                },
                error: function (data) {
                    $("#error_alert").text(data);
                    $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                }
                
            })
        }
    })

    $(document).on('click', '.submit_media_video', function(e){
        e.preventDefault(e);
        var button = $(this);  
        var file = $(button).siblings(".media_input_video").prop('files')[0];
        if(file == null){
            $("#error_alert").text("Не си одберал/а видео, или фајлот што е одберан е лош формат(не е видео)");
            $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
            $(button).siblings(".media_input_video").focus();
        }
        else{
            var data = new FormData();
            data.append('ad_video', file);
            data.append('csrfmiddlewaretoken', token);
            $.ajax({
                url: 'https://greengoshop.mk/analytics/upload-campaign-video',
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data.video_url)
                    var ad_id = data.video_id;
                    $(button).closest('.media_input').siblings('.media_holder').find('.video_media_preview').attr('src', data.video_url)
                    $(button).closest('.media_input').siblings('.media_holder').show();
                    $(button).closest('.media_input').siblings('.media_holder').find('.ad_media_video_id').val(ad_id)
                    
                    $.ajax({
                        url: 'https://greengoshop.mk/analytics/get-video-thumbnails',
                        method: 'GET',
                        data: {
                            'ad_id': ad_id,
                            'csrfmiddlewaretoken': token
                        },
                        success: function (data) {
                            var thumbnail_urls = data.thumbnail_urls
                            console.log(thumbnail_urls)
                            $.each(thumbnail_urls, function(index, thumbnail_url) {
                                console.log(thumbnail_url)
                                $(button).closest('.media_input').siblings('.media_holder').find('.thumbnail_bundles').append('<div class="col-md-3 my-2 thumbnail-container rounded"><img src="' + thumbnail_url + '" class="img-thumbnail thumbnail-option" style="cursor:pointer!important"></div>')
                            })
                        }

                        })
                },
                error: function (data) {
                    $("#error_alert").text(data);
                    $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                }
            })
        }
    })

    $(document).on('click', '.submit_media_video_thumnail', function(e){
        e.preventDefault(e);
        var button = $(this);
        var file = $(button).siblings(".media_input_video_thumbnail").prop('files')[0];
        if(file == null){
            $("#error_alert").text("Не си одберал/а слика, или сликата е лош формат(дозволени се само: .jpg, .png, .jpeg)");
            $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
            $(button).siblings(".media_input_photo").focus();
        }
        else{
            var data = new FormData();
            data.append('ad_image', file);
            data.append('csrfmiddlewaretoken', token);
            $.ajax({
                url: 'https://greengoshop.mk/analytics/upload-campaign-photo',
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data.image_url)
                    $(button).closest('.media_input').siblings('.media_holder').find('.thumbnail_media_preview').attr('src', data.image_url)
                    $(button).closest('.media_input').siblings('.media_holder').find('.thumbnail_bundles').find('.thumbnail-container').removeClass('border border-dark active_thumbnail')
                    $(button).closest('.media_input').siblings('.media_holder').find('.thumbnail_bundles').append('<div class="col-md-3 my-2 thumbnail-container rounded custom_thumbnail active_thumbnail border border-dark"><img src="' + data.image_url + '" class="img-thumbnail thumbnail-option" style="cursor:pointer!important"></div>')
                },
                error: function (data) {
                    $("#error_alert").text(data);
                    $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                }
                
            })
        }
    })
    $(document).on('click', '.thumbnail-option', function(e){
        $(this).closest('.thumbnail-container').siblings().removeClass('border border-dark active_thumbnail')
        $(this).closest('.thumbnail-container').addClass('border border-dark active_thumbnail')
        $(this).closest('.thumbnail_bundles').siblings('.main-thumbnail-row').find('.thumbnail_media_preview').attr('src', $(this).attr('src'))
        
    })

    $(document).on('click', '.search_audiences_btn', function(e){
        e.preventDefault(e);
        var button = $(this);
        var search_term = $(button).closest('.search_audiences_btn_container').siblings('.search_audience_input').val();
        if(search_term == ''){
            $("#error_alert").text("Немаш внесено ништо за пребарување");
            $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
            $(button).closest('.search_audiences_btn_container').siblings('.search_audience_input').focus();
        }
        else{
            $.ajax({
                url: 'https://greengoshop.mk/analytics/search-ad-audiences',
                method: 'GET',
                data: {
                    'search_term': search_term,
                    'csrfmiddlewaretoken': token
                },
                success: function (data) {
                    // loop over all audience-select-value elements and append options from data
                    var audiences = data.audiences

                    $(".dropdown-menu").each(function(index, element){
                        $.each(audiences, function(index, audience) {
                            $(element).append('<li class="dropdown-item"><input type="hidden" name="aud_id" class="audience_id" value=' + audience.id + '>' + '<input type="hidden" name="aud_name" class="audience_name" value=' + audience.name + '>' + audience.adset_name + '</li>')
                        })
                    })
                    
                }
            })
        }
    })
    
    $(document).on('click', '.video_generate_thumbnail_btn', function(e){
        var button = $(this)
        var video = $(this).closest('.thumbnail_bundles').siblings('.main-thumbnail-row').find('.video_media_preview');
        // get current time of video
        var current_time = video[0].currentTime;
        var ad_id = $(button).siblings('.ad_media_video_id').val();
        $.ajax({
            url: 'https://greengoshop.mk/analytics/generate-ad-video-thumbnail',
            method: 'GET',
            data: {
                'ad_id': ad_id,
                'current_time': current_time,
                'csrfmiddlewaretoken': token
            },
            success: function (data) {
                console.log(data.thumbnail_url)
                $(button).closest('.thumbnail_bundles').siblings('.main-thumbnail-row').find('.thumbnail_media_preview').attr('src', data.thumbnail_url)
                $(button).closest('.thumbnail_bundles').siblings('.main-thumbnail-row').find('.thumbnail_bundles').append('<div class="col-md-3 my-2 thumbnail-container custom_thumbnail rounded"><img src="' + data.thumbnail_url + '" class="img-thumbnail thumbnail-option" style="cursor:pointer!important"></div>')
            }
        })


    })
    
    $(document).on('click', '.dropdown-item', function(e){
        console.log('option');
        var option = $(this);
        var audience_id = $(option).children('.audience_id').val();
        var audience_name = $(option).children('.audience_name').val();
        $(option).siblings().removeClass('selected');
        $(option).addClass('selected');
        $(option).closest('.adset_template').find('.adset_name_input').val($(option).text());
        $(option).closest('.audience_selecting_place').find('.chosen_ad_audience').val($(option).text())
        $(option).closest('.audience_selecting_place').find('.adset_audience_id_input').val(audience_id)
        $(option).closest('.audience_selecting_place').find('.adset_audience_name_input').val(audience_name)
    })



    function validate_all_inputs(){
        var form_is_valid = true;
        if($("#campaign_name").val().length == 0){
            $("#campaign_name").removeClass('border-primary')
            $("#campaign_name").addClass('border-danger')
            form_is_valid = false;
        }
        if($("#chosen_product").val().length == 0){
            $("#product_dropdown_search").addClass('border-danger')
            form_is_valid = false;
        }
        // loop over every adset and  log all inputs with class adset_budget_input

        var adsets_inputs = $(".adset_template");
        $.each(adsets_inputs, function(index, adset){
            if($(adset).find('.adset_budget_input').val().length == 0){
                $(adset).find('.adset_budget_input').removeClass('border-dark')
                $(adset).find('.adset_budget_input').addClass('border-danger')
                form_is_valid = false;
            }
            if($(adset).find('.adset_minage_input').val().length == 0){
                $(adset).find('.adset_minage_input').removeClass('border-dark')
                $(adset).find('.adset_minage_input').addClass('border-danger')
                form_is_valid = false;
            }
            if($(adset).find('.adset_maxage_input').val().length == 0){
                $(adset).find('.adset_maxage_input').removeClass('border-dark')
                $(adset).find('.adset_maxage_input').addClass('border-danger')
                form_is_valid = false;
            }
            if($(adset).find('.adset_name_input').val().length == 0){
                $(adset).find('.adset_name_input').removeClass('border-dark')
                $(adset).find('.adset_name_input').addClass('border-danger')
                form_is_valid = false;
            }
            if($(adset).find('.adset_audience_id_input').val().length == 0){
                $(adset).find('.adset_audience_input').removeClass('border-dark')
                $(adset).find('.adset_audience_input').addClass('border-danger')
                form_is_valid = false;
            }
            if($(adset).find('.adset_audience_name_input').val().length == 0){
                $(adset).find('.adset_audience_input').removeClass('border-dark')
                $(adset).find('.adset_audience_input').addClass('border-danger')
                form_is_valid = false;
            }
            var adset_ads = $(adset).find('.adset_ad_input');
            $.each(adset_ads, function(index, ad){
                if($(ad).find('.ad_primary_text_input').val().length == 0){
                    $(ad).find('.ad_primary_text_input').removeClass('border-primary')
                    $(ad).find('.ad_primary_text_input').addClass('border-danger')
                    form_is_valid = false;
                }
                if($(ad).find('.ad_headline_input').val().length == 0){
                    $(ad).find('.ad_headline_input').removeClass('border-primary')
                    $(ad).find('.ad_headline_input').addClass('border-danger')
                    form_is_valid = false;
                }

                if($(ad).find('.ad_description_input').val().length == 0){
                    $(ad).find('.ad_description_input').removeClass('border-primary')
                    $(ad).find('.ad_description_input').addClass('border-danger')
                    form_is_valid = false;
                }
                if($(ad).find('.media_type_photo_btn').hasClass('btn-success')){
                    if($(ad).find(".ad_type_photo_input").attr('src') == ''){
                        $(ad).find('.media_input_photo').removeClass('border-primary')
                        $(ad).find('.media_input_photo').addClass('border-danger')
                        form_is_valid = false;
                    }
                }
                if($(ad).find('.media_type_video_btn').hasClass('btn-success')){
                    if($(ad).find(".ad_type_video_input").attr('src') == ''){
                        $(ad).find('.media_input_video').removeClass('border-primary')
                        $(ad).find('.media_input_video').addClass('border-danger')
                        form_is_valid = false;
                    }
                    if($(ad).find(".ad_type_video_thumbnail_input").attr('src') == ''){
                        $(ad).find('.video_generate_thumbnail_btn').removeClass("btn-primary")
                        $(ad).find('.video_generate_thumbnail_btn').addClass("btn-danger")
                        form_is_valid = false;
                    }
                }
            })


        })
        
        return form_is_valid;

    }

    $(document).on('click', '#create_campaign', function(e){
        var button = $(this)
        if(button.hasClass('disabled')){
            console.log('button is disabled')
        }
        console.log('clicked on create campaign')
        e.preventDefault(e);

        if(validate_all_inputs()){
            var campaign_name = $("#campaign_name").val();
            var product_id = $("#chosen_product").val();
            var adsets = [];
            var adsets_inputs = $(".adset_template");
            // loop over every adset and  log all inputs with class adset_budget_input
            $.each(adsets_inputs, function(index, adset){
                // find input with class adset_budget and store it as dict with key budget
                var photo_counter = 1;
                var video_counter = 1;
                var adset_ads = [];
                var adset_ads_inputs = $(adset).find('.adset_ad_input');
                var genders = [];
                var adset_budget = $(adset).find('.adset_budget_input').val();
                var adset_minage = $(adset).find('.adset_minage_input').val();
                var adset_maxage = $(adset).find('.adset_maxage_input').val();
                var adset_audience_id = $(adset).find('.adset_audience_id_input').val();
                var adset_audience_name = $(adset).find('.adset_audience_name_input').val();
                var adset_name = $(adset).find('.adset_name_input').val();
                var adset_dict = {
                    'adset_budget': adset_budget,
                    'adset_minage': adset_minage,
                    'adset_maxage': adset_maxage,
                    'adset_audience_id': adset_audience_id,
                    'adset_audience_name': adset_audience_name,
                    'adset_name': adset_name,
                }
                if(!$(adset).find('.adset_male_input').prop('checked') && $(adset).find('.adset_female_input').prop('checked')){
                    adset_dict['genders'] = [2];
                }
                if(!$(adset).find('.adset_female_input').prop('checked') && $(adset).find('.adset_male_input').prop('checked')){
                    adset_dict['genders'] = [1];
                }
                // loop over every ad in adset 
                var ad_videos_list = [];
                $.each(adset_ads_inputs, function(subindex, ad){


                    var ad_primary_text = $(ad).find('.ad_primary_text_input').val();
                    var ad_headline = $(ad).find('.ad_headline_input').val();
                    var ad_description = $(ad).find('.ad_description_input').val();
                    var ad_dict = {
                        'ad_primary_text': ad_primary_text,
                        'ad_headline': ad_headline,
                        'ad_description': ad_description,
                    }
                    if($(ad).find('.media_type_photo_btn').hasClass('btn-success')){
                        $(ad).find('.adset_ad_name_input').val('Slika ' + photo_counter)
                        photo_counter += 1;
                        console.log($(ad).find('.adset_ad_name_input').val())
                        
                        var ad_type = 'photo';
                        var ad_name = $(ad).find('.adset_ad_name_input').val();
                        var ad_image_path = $(ad).find('.ad_type_photo_input').attr('src');
                        ad_dict['ad_name'] = ad_name
                        ad_dict['ad_type'] = ad_type;
                        ad_dict['ad_image_path'] = ad_image_path;
                    }
                    else{
                        var is_included = 0
                        for(var i=0; i < ad_videos_list.length; i++){
                            console.log('LOOP')
                            console.log(ad_videos_list[i].url)
                            if(ad_videos_list[i].url == $(ad).find('.media_input_video.big-input').val()){
                                is_included = 1;
                                console.log('Found same video')
                                if($(ad).find('.thumbnail-container.manual_thumbnail.active_thumbnail').length){
                                    ad_videos_list[i].manual_thumbnail += 1;
                                    $(ad).find('.adset_ad_name_input').val('Video ' + (i+1) + ' - ' + 'Manual Thumbnail ' + ad_videos_list[i].manual_thumbnail)
                                }
                                if($(ad).find('.thumbnail-container.custom_thumbnail.active_thumbnail').length){
                                    ad_videos_list[i].custom_thumbnail += 1;
                                    $(ad).find('.adset_ad_name_input').val('Video ' + (i+1) + ' - ' + 'Custom Thumbnail ' + ad_videos_list[i].custom_thumbnail)
                                }
                            }

                        }
                        if(is_included == 0){
                            var manual_thumbnail = 0;
                            var custom_thumbnail = 0;
                            if($(ad).find('.thumbnail-container.manual_thumbnail.active_thumbnail').length){
                                manual_thumbnail = 1;
                                $(ad).find('.adset_ad_name_input').val('Video ' + (parseInt(ad_videos_list.length) + 1) + ' - ' + 'Manual Thumbnail ' + manual_thumbnail)
                            }
                            if($(ad).find('.thumbnail-container.custom_thumbnail.active_thumbnail').length){
                                custom_thumbnail = 1;
                                $(ad).find('.adset_ad_name_input').val('Video ' + (parseInt(ad_videos_list.length) + 1) + ' - ' + 'Custom Thumbnail ' + custom_thumbnail)
                            }

                            ad_videos_list.push({
                                'url': $(ad).find('.media_input_video.big-input').val(),
                                'manual_thumbnail': manual_thumbnail,
                                'custom_thumbnail': custom_thumbnail
                            })
                        }

                        
                        var ad_type = 'video';
                        var ad_name = $(ad).find('.adset_ad_name_input').val();
                        var ad_video_path = $(ad).find('.ad_type_video_input').attr('src');
                        var thumbnail_path = $(ad).find('.ad_type_video_thumbnail_input').attr('src');
                        ad_dict['ad_name'] = ad_name
                        ad_dict['ad_type'] = ad_type;
                        ad_dict['ad_video_path'] = ad_video_path;
                        ad_dict['thumbnail_path'] = thumbnail_path;
                    }
                    adset_ads.push(ad_dict);
                })
                
                
                adset_dict['ads'] = adset_ads;
                adsets.push(adset_dict);
                
            })
            console.log(adsets, product_id, campaign_name)
            $(button).addClass('disabled')
            $(button).html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> Се креира...')
           
            $.ajax({
                url: 'https://greengoshop.mk/analytics/create-campaign',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': token,
                    'campaign_name': campaign_name,
                    'product_id': product_id,
                    'adsets': JSON.stringify(adsets),
                },
                success: function(response){
                    $("#success_alert").text("Успешно креирана кампања!");
                    $("#success_alert").fadeIn(100);
                    $(button).html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> Додавање на Campaign ID на продуктот...')
                    console.log(response.campaign_id)
                    $.ajax({
                        url: 'https://greengoshop.mk/analytics/save-new-campaign-id',
                        type: 'POST',
                        data: {
                            'csrfmiddlewaretoken': token,
                            'campaign_id': response.campaign_id,
                            'product_id': product_id,
                        },
                        success: function(response){
                            setTimeout(function() {
                                location.reload(true)
                            }, 3000);
                        }
                    }) 
                },
                error: function(data) {
                    $("#error_alert").text(data.responseJSON.error);
                    $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                    $(button).removeClass('disabled')
                    $(button).html('Креирај кампања')
                  }
                

                
            })
              
            }
        else{
            $("#error_alert").text("Полињата обележани со црвено се задолжителни!");
            $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                
        }
        
    })
    $(document).on("click", ".create_ad_preview" ,function(){
        var button = $(this)
        var ad_primary_text = $(this).closest('.ad').find('.ad_primary_text_input').val();
        var ad_headline = $(this).closest('.ad').find('.ad_headline_input').val();
        var ad_description = $(this).closest('.ad').find('.ad_description_input').val();
        console.log(ad_primary_text, ad_headline, ad_description)
        var photo_url = '';
        if($(button).hasClass("ad_type_is_photo")){
            if($(this).closest('.ad').find('.ad_type_photo_input').attr('src') == ''){
                $("#error_alert").text("Немаш одберано слика за preview!");
                $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                return;
            }
            photo_url = $(this).closest('.ad').find('.ad_type_photo_input').attr('src');
            
        }
        else{
            if($(this).closest('.ad').find('.ad_type_video_input').attr('src') == ''){
                $("#error_alert").text("Немаш одберано video за preview!");
                $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                return;
            }
            if($(this).closest('.ad').find('.ad_type_video_thumbnail_input').attr('src') == ''){
                $("#error_alert").text("Немаш одберано слика за preview!");
                $("#error_alert").fadeIn(100).delay(7000).fadeOut(100);
                return;
            }
            photo_url = $(this).closest('.ad').find('.ad_type_video_thumbnail_input').attr('src');
        }
        console.log('ad_prev')
        $.ajax({
            url: 'https://greengoshop.mk/analytics/get-ad-preview',
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': token,
                'ad_primary_text': ad_primary_text,
                'ad_headline_text': ad_headline,
                'ad_description_text': ad_description,
                'photo_url': photo_url,
            },
            success: function(response){
                var tempElement = document.createElement('div');
                tempElement.innerHTML = response['ad_preview'];
                $(".iframe_holder").empty();
                $(".iframe_holder").append(tempElement.firstChild);
            },

        })
    })
});

