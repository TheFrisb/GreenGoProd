console.log("WOO")

const hamburger = document.querySelector(".header-search-icon")
const navMenu = document.querySelector("#navigation")
$(document).ready(function() {
    function cache_clear() {
        window.location.reload(true);
    }
    setInterval(function() {
        cache_clear()
      }, 180000);
    $('.confirm-orderBtn').click(function (e){
        e.preventDefault();
        var confirmBtn = $(this);
        var order_id = $(this).closest('.order-td').find('.order_id').val();

        var token = $('input[name=csrfmiddlewaretoken]').val()
        console.log(token)
        $.ajax({
            method: "POST",
            url: "/update-order",
            data: {
                'orderId': order_id,
                'action': 'confirm',
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                $(confirmBtn).closest("tr").addClass("confirmed-row").hide(1500, "swing");
                $(confirmBtn).closest("td").find("span").text("Потврдена")
            }
        })
    })
    $('.delete-orderBtn').click(function (e){
        e.preventDefault();
        var deleteBtn = $(this);
        var order_id = $(this).closest('.order-td').find('.order_id').val();

        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        console.log($(this))
        console.log(token);
        $.ajax({
            method: "POST",
            url: "/update-order",
            data: {
                'orderId': order_id,
                'action': 'delete',
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                $(deleteBtn).closest("tr").addClass("removed-row").hide(1500, "swing");
                $(deleteBtn).closest("td").find("span").text("Избришена")
            }   
        })
    })
    $('.return-orderBtn').click(function (e){
        e.preventDefault();
        var returnBtn = $(this);
        var order_id = $(this).closest('.order-td').find('.order_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        console.log($(this))
        console.log(token);
        $.ajax({
            method: "POST",
            url: "/update-order",
            data: {
                'orderId': order_id,
                'action': 'return',
                csrfmiddlewaretoken: token,
            },
            
            success: function (response){
                $(returnBtn).closest("tr").addClass("blank-row").hide(1500, "swing");
                $(returnBtn).closest("td").find("span").text("Вратена")
            }
        })
    })
    $(".remove_abandoned_cart").click(function (e){
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var cart_id = $(this).data("order-id")
        var btn = $(this)
        console.log('Clicked')
        $.ajax({
            method: "POST",
            url: "/remove-abandoned-cart",
            data:{
                'cartId': cart_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response){
                $(btn).closest("tr").addClass("table-dark").fadeOut(4000);
            }
        })
    })
    $('[data-toggle="tooltip"]').tooltip()
    
    
 })
 
  
  
  
