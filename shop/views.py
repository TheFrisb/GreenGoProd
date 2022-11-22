from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import *

import datetime

# Create your views here.



def ProductListView(request):
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("WA")
    
    cart = Cart.objects.filter(user=request.user)
    total = 0
    if cart:
        for item in cart:
            total = total + (item.product.sale_price * item.product_qty)
    context = {
        'products': Product.objects.all,
        'title': 'Почетна',
        'categories': Category.objects.all,
        'cart': cart,
        'cart_total': total,
        }
    return render(request, 'shop/home.html', context)


def Categories(request):
    category = Category.objects.all
    context = {'category': category}
    render(request, "shop/category.html", context)

def CategoryView(request, slug):
    if(Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        
        context = {
            'products': products, 
            'categories': Category.objects.all
            }
        return render(request, "shop/home.html", context)
    else:
        messages.warning(request, "Линкот што го следевте не постои")
        return redirect('shop-home')


def ProductView(request, slug):
    cart = Cart.objects.filter(user=request.user)
    total = 0
    if cart:
        for item in cart:
            total = total + (item.product.sale_price * item.product_qty)

    if(Product.objects.filter(slug=slug)):
        attributes = ProductAttribute.objects.filter(product__slug=slug)
        gallery = ProductGallery.objects.filter(product__slug=slug)
        product = Product.objects.filter(slug=slug).first
        if(Review.objects.filter(product__slug=slug)):
            reviews = Review.objects.filter(product__slug=slug)

            reviewsaverage = 0
            count = 0
            for i in reviews:
                reviewsaverage += int(i.rating)
                count += 1
            reviewsaverage = reviewsaverage // count

            context = {
                'product': product,
                'reviews': reviews,
                'cart': cart,
                'cart_total': total,
                'ratingaverage': reviewsaverage,
                'reviewcount': count,
                'slider1': Product.objects.filter(category__name='ЗАЛИХА')[:8],
                'slider2': Product.objects.all()[:8],
            }
        else:
            context = {
                'product': product,
                'cart': cart,
                'cart_total': total,
                'slider1': Product.objects.filter(category__name='ЗАЛИХА')[:8],
                'slider2': Product.objects.all()[:8],
                'attributes' : attributes,
                'gallery': gallery,
            }


        return render(request, "shop/product-page.html", context)
    else:
        messages.warning(request, "Линкот што го следевте не постои")
        return redirect('shop-home')


def CheckoutView(request):
    cart = Cart.objects.filter(user=request.user)
    context = {
        'cart': cart,
        'title': 'Кон Нарачка',
        }

    return render(request, 'shop/checkout.html', context)


def ThankYouView(request, slug):
    if(Order.objects.filter(tracking_no=slug)):
        order = Order.objects.filter(tracking_no=slug).first
        orderItems = OrderItem.objects.filter(order__tracking_no=slug) # Sql join ?
    context = {
        'order': order,
        'orderItems': orderItems,
    }

    return render(request, 'shop/thank-you.html', context)




class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/home.html'
    extra_context = {
        'title' : "Почетна"
    }
    context_object_name = 'products'
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ) 
        return object_list
    



def login_shopmanager(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("shopmanagerhome")
    else:
        context = {
                'title': 'Login',
            }
        if request.method =='POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("shopmanagerhome")
            else:
                messages.error(request, "Invalid username or Password")
                return redirect('/')
        return render(request, "shop/shopmanager/login.html", context)


def logout_shopmanager(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
    
    return redirect("/")
    


def shopmanager_dashboard(request):
    orders = Order.objects.filter(status='Pending').order_by('-id')[:50]
    orderItems = OrderItem.objects.filter(order__status = 'Pending')
    title = 'НЕПОТВРДЕНИ НАРАЧКИ'
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'heading' : title,
        'order_status': 'Непотврдена',
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_confirmed(request):
    orders = Order.objects.filter(status='Confirmed')
    orderItems = OrderItem.objects.filter(order__status = 'Confirmed')
    title = 'ПОТВРДЕНИ НАРАЧКИ'
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'heading' : title,
        'order_status': 'Потврдена',
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_deleted(request):
    orders = Order.objects.filter(status='Deleted').order_by('-updated_at')[:50]
    orderItems = OrderItem.objects.filter(order__status = 'Deleted')
    title = 'ИЗБРИШЕНИ НАРАЧКИ'
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'heading' : title,
        'order_status': 'Избришена',
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_create_order(request):
    context = {
        'heading': 'Креири нарачка'
    }

    return render(request, 'shop/shopmanager/create_order.html', context)

def Dostava(request):
    context = {
        'title': 'Политика за достава'
    }
    return render(request, 'shop/policies/dostava.html', context)


def Reklamacija(request):
    context = {
        'title': 'Политика за рекламација'
    }
    return render(request, 'shop/policies/reklamacija.html', context)


def Pravila_Na_Koristenje(request):
    context = {
        'title': 'Правила на користење'
    }
    return render(request, 'shop/policies/pravila_na_koristenje.html', context)

def Cookies_Page(request):
    context = {
        'title': 'Политика за приватност и колачиња'
    }
    return render(request, 'shop/policies/politika_na_privatnost_i_kolacinja.html', context)