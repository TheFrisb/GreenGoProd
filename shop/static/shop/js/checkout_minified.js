function create_custom_dropdowns(){$("select").each(function(t,e){if(!$(this).next().hasClass("dropdown-select")){$(this).after('<div class="dropdown-select wide '+($(this).attr("class")||"")+'" tabindex="0"><span class="current"></span><div class="list"><ul></ul></div></div>');var s=$(this).next();window.matchMedia("(max-width: 767px)").matches&&$(s).addClass("ismobile");var i=$(e).find("option"),o=$(this).find("option:selected");s.find(".current").html(o.data("display-text")||o.text()),i.each(function(t,e){var i=$(e).data("display-text")||"";s.find("ul").append('<li class="option '+($(e).is(":selected")?"selected":"")+'" data-value="'+$(e).val()+'" data-display-text="'+i+'">'+$(e).text()+"</li>")})}}),$(".dropdown-select ul").before('<div class="dd-search"><input id="txtSearchValue" autocomplete="off" onkeyup="filter()" class="dd-searchbox" type="text"></div>')}function filter(){var t=$("#txtSearchValue").val();$(".dropdown-select ul > li").each(function(){$(this).text().toLowerCase().indexOf(t.toLowerCase())>-1?$(this).show():$(this).hide()})}$(document).on("click",".dropdown-select",function(t){!$(t.target).hasClass("dd-searchbox")&&($(".dropdown-select").not($(this)).removeClass("open"),$(this).toggleClass("open"),$(this).hasClass("open")?($(this).find(".option").attr("tabindex",0),$(this).find(".selected").focus(),$("#txtSearchValue").focus(),$(this).hasClass("ismobile")&&$("html, body").animate({scrollTop:$(this).offset().top-100},800)):($(this).find(".option").removeAttr("tabindex"),$(this).focus()))}),$(document).on("click",function(t){0===$(t.target).closest(".dropdown-select").length&&($(".dropdown-select").removeClass("open"),$(".dropdown-select .option").removeAttr("tabindex")),t.stopPropagation()}),$(document).on("click",".dropdown-select .option",function(t){input=$(".checkout-city"),console.log(input),$(this).closest(".list").find(".selected").removeClass("selected"),$(this).addClass("selected");var e=$(this).data("display-text")||$(this).text();$(this).closest(".dropdown-select").find(".current").text(e),$(this).closest(".dropdown-select").prev("select").val($(this).data("value")).trigger("change"),$(input).val(e)}),$(document).on("keydown",".dropdown-select",function(t){var e=$($(this).find(".list .option:focus")[0]||$(this).find(".list .option.selected")[0]);if(13==t.keyCode)return $(this).hasClass("open")?e.trigger("click"):$(this).trigger("click"),!1;if(40==t.keyCode)return $(this).hasClass("open")?e.next().focus():$(this).trigger("click"),!1;if(38==t.keyCode){if($(this).hasClass("open")){var e=$($(this).find(".list .option:focus")[0]||$(this).find(".list .option.selected")[0]);e.prev().focus()}else $(this).trigger("click");return!1}if(27==t.keyCode)return $(this).hasClass("open")&&$(this).trigger("click"),!1}),$(document).ready(function(){create_custom_dropdowns()});
