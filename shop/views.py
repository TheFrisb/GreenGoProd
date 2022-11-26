from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.db.models import CharField, Value, Case, Value, When, Q, Func, F
from django.db.models import Q
from .models import *
from django.core.paginator import Paginator
from django.db.models.functions import Cast
import uuid
from uuid import  uuid4
import datetime
import xlwt
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.db.models.functions import Concat

# Create your views here.



def ProductListView(request):
    products = Product.objects.all()
    paginator = Paginator(products, 16)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    total = 0
    context = {
        'products': products,
        'title': 'Почетна',
        }
    
    
    return render(request, 'shop/home.html', context)


def CategoryView(request, slug):
    if(Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        paginator = Paginator(products, 16)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        
        context = {
            'products': products, 
            'categories': Category.objects.all,
            }
        
        return render(request, "shop/home.html", context)
    else:
        messages.warning(request, "Линкот што го следевте не постои")
        return redirect('shop-home')


def ProductView(request, slug):

    if(Product.objects.filter(slug=slug)):
        attributes = ProductAttribute.objects.filter(product__slug=slug)
        gallery = ProductGallery.objects.filter(product__slug=slug)
        product = Product.objects.filter(slug=slug).first
        cartOffers = CartOffers.objects.all()
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
                'ratingaverage': reviewsaverage,
                'reviewcount': count,
                'slider1': Product.objects.filter(category__name='ЗАЛИХА')[:8],
                'slider2': Product.objects.all()[:8],
            }
        else:
            context = {
                'product': product,
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
    orderFees = CheckoutFees.objects.all()
    cartHolder = Cart.objects.get(session = request.session['nonuser'])
    cartFees = CartFees.objects.filter(cart=cartHolder)
    feetotal = 0
    for orderfee in orderFees:
        for cartfee in cartFees:
            if(orderfee == cartfee.fee):
                orderfee.is_added = True
                feetotal += cartfee.price
    
    context = {
        'title': 'Кон Нарачка',
        'orderFees': orderFees,
        'cartFees': cartFees,
        'feetotal': feetotal,
        }

    return render(request, 'shop/checkout.html', context)


def ThankYouView(request, slug):
    if(Order.objects.filter(tracking_no=slug)):
        order = Order.objects.filter(tracking_no=slug).first
        orderItems = OrderItem.objects.filter(order__tracking_no=slug) # Sql join ?
        offerproduct = orderItems.reverse()[0]
        orderFees = OrderFeesItem.objects.filter(order__tracking_no=slug)
        feetotal = 0
        for fee in orderFees:
            feetotal += fee.price

    context = {
        'order': order,
        'orderItems': orderItems,
        'offerproduct': offerproduct,
        'orderFees': orderFees,
        'feetotal': feetotal
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


def export_excel(request):

    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename=Expenses.xls'#+  str(datetime.datetime.now())+ '.xls'

    # wb= xlwt.Workbook(encoding='utf-8')
    # ws= wb.add_sheet('Expenses')
    # row_num = 0
    # font_style=xlwt.XFStyle()
    # font_style.font.bold=True

    ## columns = ['DATA NA PORACKA', 'IME I PREZIME', 'ADRESA', 'GRAD', 'TELEFON', 'FEES', 'VKUPNO', 'DOSTAVA', 'KOLICINA', 'IME NA PRODUKT', 'LABEL', 'CENA NA PRODUKT']

    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style)

    # font_style=xlwt.XFStyle()

    # rows = OrderItem.objects.all().values_list(
    #     'product__thumbnail', 'label')
    
    # for row in rows:
    #     row_num+=1

    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, str(row[col_num]), font_style)

    # wb.save(response)

    #rows = OrderItem.objects.all().values_list(
      #      'product__thumbnail', 'label')
    #return response

# orderitem order product  price  quantity  label  supplier attribute_name  attribute_price
 #order user name address city  number  subtotal_price total_price shipping shipping_price 
    # orderstatuses = (
    #     ('Pending', 'Pending'),
    #     ('Confirmed', 'Confirmed'),
    #     ('Refunded', 'Refunded'),
    #     ('Deleted', 'Deleted')
    # )
#status message tracking_no created_at updated_at
#Cast('order__created_at', CharField()) )
    workbook = Workbook()
    worksheet = workbook.active
    row_num = 1
    worksheet.column_dimensions['A'].width = 20
    worksheet.column_dimensions['B'].width = 35
    worksheet.column_dimensions['C'].width = 35
    worksheet.column_dimensions['D'].width = 20
    worksheet.column_dimensions['E'].width = 20
    worksheet.column_dimensions['F'].width = 20
    worksheet.column_dimensions['G'].width = 20
    worksheet.column_dimensions['H'].width = 20
    worksheet.column_dimensions['I'].width = 10
    worksheet.column_dimensions['J'].width = 55
    worksheet.column_dimensions['K'].width = 55
    worksheet.column_dimensions['L'].width = 20
    worksheet.column_dimensions['L'].width = 20
    worksheet.column_dimensions['M'].width = 100
    columns = ['DATA NA PORACKA', 'IME I PREZIME', 'ADRESA', 'GRAD', 'TELEFON', 'FEES', 'VKUPNO', 'DOSTAVA', 'KOLICINA', 'IME NA PRODUKT', 'LABEL', 'CENA NA PRODUKT']
    for col_num in range(1, len(columns)+1):
        
        cell =  worksheet.cell(row=row_num, column=col_num, value=columns[col_num - 1])
# ... worksheet.append(...) all of your data ...
    rows = OrderItem.objects.filter(Q(order__status = 'Confirmed') | Q(order__status = 'Pending')).annotate(
        shipping = Case(
            When(order__shipping = True, then=Value('do vrata 130 den')),
            When(order__shipping = False, then=Value('besplatna dostava'))
        ),
        full_product_title = Concat('product__title', Value(' '), 'attribute_name' )).order_by('-order__created_at').values_list( 'order__created_at', 'order__name', 'order__address', 'order__city', 'order__number', 'order__number', 'order__total_price', 'shipping', 'quantity',
    'full_product_title', 'label', 'price', 'order__message')
    print(rows)
   
    for row in rows:
        row_num += 1
        for col_num in range(1, len(row)+1):
            if(col_num == 1):
                cell =  worksheet.cell(row=row_num, column=col_num).value = (row[col_num-1].strftime("%d.%y.%Y, %H:%M"))
            else:
                cell =  worksheet.cell(row=row_num, column=col_num).value = str(row[col_num-1])


    response = HttpResponse(content=save_virtual_workbook(workbook))
    response['Content-Disposition'] = 'attachment; filename=eksport_' + str(datetime.datetime.now()) + '.xlsx'
    return response
