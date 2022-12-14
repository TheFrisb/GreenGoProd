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
from openpyxl.styles import Alignment, Font
from openpyxl.writer.excel import save_virtual_workbook
from django.db.models.functions import Concat
from .forms import ExportOrder
from django.utils.timezone import get_current_timezone, make_aware
import csv
from django.utils.html import strip_tags
from .controller import facebook_pixel
# Create your views here.


def export_products_csv(request):
    products = Product.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Description', 'Link', 'Image Link', 'Availability', 'Price', 'Condition', 'Brand'])

    for product in products:
        content = strip_tags(product.content).replace('&nbsp;', '')
        content = os.linesep.join([s for s in content.splitlines() if s])
        if product.status == 'VARIABLE':
            attributes = ProductAttribute.objects.filter(product=product)
            for attribute in attributes:
                attribute_name = ''
                if(attribute.color is not None):
                    attribute_name = attribute.color.title

                if(attribute.size is not None):
                    attribute_name = attribute.size.title

                if(attribute.offer is not None):
                    attribute_name = attribute.offer.title
                
                writer.writerow([str(product.id) + '_' + attribute.label, product.title + ' - ' + attribute_name, content , 'https://greengoshop.mk' + product.get_absolute_url(), 'https://greengoshop.mk' + product.thumbnail.url, 'in stock', str(product.sale_price) + 'MKD', 'New', 'GreenGoShopMK'])
        
        writer.writerow([product.id, product.title, content , 'https://greengoshop.mk' + product.get_absolute_url(), 'https://greengoshop.mk' + product.thumbnail.url, 'in stock', str(product.sale_price) + 'MKD', 'New', 'GreenGoShopMK'])

    return response



def ProductListView(request):
    products = Product.objects.filter(status__in=['PUBLISHED','VARIABLE']).order_by('-date_posted')
    paginator = Paginator(products, 16)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    total = 0
    context = {
        'products': products,
        'title': '??????????????',
        }
    
    
    return render(request, 'shop/home.html', context)


def CategoryView(request, slug):
    if(Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug).order_by('-date_posted')
        paginator = Paginator(products, 16)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        title = Category.objects.get(slug = slug).name
        
        context = {
            'products': products, 
            'title': title,
            }
        
        return render(request, "shop/home.html", context)
    else:
        messages.warning(request, "???????????? ?????? ???? ???????????????? ???? ????????????")
        return redirect('shop-home')


def ProductView(request, slug):
    now = datetime.datetime.now()
    current_day = now.weekday()
    mapped_delivery_days = {
        0: ['??????????', '??????????'],
        1: ['????????????????', '????????????'],
        2: ['??????????', '????????????????????'],
        3: ['????????????', '??????????????'],
        4: ['????????????????????', '??????????'],
        5: ['??????????????', '????????????????'],
        6: ['??????????????', '????????????????'],
    }
    delivery_days = mapped_delivery_days[current_day]
    try:
        attributes = ProductAttribute.objects.filter(product__slug=slug)
        gallery = ProductGallery.objects.filter(product__slug=slug)
        product = Product.objects.get(slug=slug)
        if product.review_average != 0:
            reviews = Review.objects.filter(product__slug=slug)
        title = product.title
        percentage = 100 - int(product.sale_price / product.regular_price * 100)
        money_saved = product.regular_price - product.sale_price
        if(product.status != 'PRIVATE'):
            if(product.review_average != 0):
                count = reviews.count()

                context = {
                    'product': product,
                    'reviews': reviews,
                    'reviewcount': count,
                    'slider1': Product.objects.filter(category__name='????????????')[:8],
                    'slider2': Product.objects.all()[:8],
                    'gallery': gallery,
                    'attributes' : attributes,
                    'title': title,
                    'percentage': percentage,
                    'money_saved': money_saved,
                    'delivery_days': delivery_days,
                }
            else:
                context = {
                    'product': product,
                    'slider1': Product.objects.filter(category__name='????????????')[:8],
                    'slider2': Product.objects.all()[:8],
                    'attributes' : attributes,
                    'gallery': gallery,
                    'title': title,
                    'percentage': percentage,
                    'money_saved': money_saved,
                    'delivery_days': delivery_days,
                }


            return render(request, "shop/product-page.html", context)
        else:
            return redirect('shop-home')
    except:
        messages.warning(request, "???????????? ?????? ???? ???????????????? ???? ????????????")
        return redirect('shop-home')


def CheckoutView(request):
    orderFees = CheckoutFees.objects.all()
    try:
        facebook_pixel.InitiateCheckoutEvent(request)
    except:
        pass
    try:
        cartFees = CartFees.objects.filter(cart__session=request.session['nonuser'])
    except:
        cartFees = None
    
    feetotal = 0
    for orderfee in orderFees:
        for cartfee in cartFees:
            if(orderfee == cartfee.fee):
                orderfee.is_added = True
                feetotal += cartfee.price
    
    context = {
        'title': '?????? ??????????????',
        'orderFees': orderFees,
        'cartFees': cartFees,
        'feetotal': feetotal,
        }

    return render(request, 'shop/checkout.html', context)


def ThankYouView(request, slug):
    order = Order.objects.filter(tracking_no=slug).first
    if(order):   
        orderItems = OrderItem.objects.filter(order__tracking_no=slug) # Sql join ?
        offerproduct = orderItems.reverse()[0]
        if offerproduct.attribute_price is not None:
            offerproduct.attribute_price = offerproduct.attribute_price - offerproduct.attribute_price * 20 // 100 
        else:
            offerproduct.price = offerproduct.price - offerproduct.price * 20 // 100 
        orderFees = OrderFeesItem.objects.filter(order__tracking_no=slug)
        feetotal = 0
        for fee in orderFees:
            feetotal += fee.price
    title = '???? ??????????????????????!'
    context = {
        'order': order,
        'orderItems': orderItems,
        'offerproduct': offerproduct,
        'orderFees': orderFees,
        'feetotal': feetotal,
        'title': title,
    }

    return render(request, 'shop/thank-you.html', context)




class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/home.html'
    extra_context = {
        'title' : "????????????"
    }
    context_object_name = 'products'
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(title__icontains=query, status__in=['PUBLISHED','VARIABLE'])
        
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
    orderItems = OrderItem.objects.filter(order__status = 'Pending').order_by('-id')
    orderfees = OrderFeesItem.objects.filter(order__status = 'Pending').order_by('-id')
    title = '?????????????????????? ??????????????'
    form = ExportOrder()
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'orderFees': orderfees,
        'heading' : title,
        'order_status': '??????????????????????',
        'form': form,
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_confirmed(request):
    orders = Order.objects.filter(status='Confirmed').order_by('-updated_at')[:50]
    orderItems = OrderItem.objects.filter(order__status = 'Confirmed').order_by('-id')
    orderfees = OrderFeesItem.objects.filter(order__status = 'Confirmed').order_by('-id')
    title = '?????????????????? ??????????????'
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'orderFees': orderfees,
        'heading' : title,
        'order_status': '??????????????????',
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_deleted(request):
    orders = Order.objects.filter(status='Deleted').order_by('-updated_at')[:50]
    orderItems = OrderItem.objects.filter(order__status = 'Deleted').order_by('-id')
    orderfees = OrderFeesItem.objects.filter(order__status = 'Deleted').order_by('-id')
    title = '?????????????????? ??????????????'
    context = {
        'orders' : orders,
        'orderItems': orderItems,
        'orderFees': orderfees,
        'heading' : title,
        'order_status': '??????????????????',
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


def shopmanager_create_order(request):
    context = {
        'heading': '???????????? ??????????????'
    }

    return render(request, 'shop/shopmanager/create_order.html', context)

def Dostava(request):
    context = {
        'title': '???????????????? ???? ??????????????'
    }
    return render(request, 'shop/policies/dostava.html', context)


def Reklamacija(request):
    context = {
        'title': '???????????????? ???? ??????????????????????'
    }
    return render(request, 'shop/policies/reklamacija.html', context)


def Pravila_Na_Koristenje(request):
    context = {
        'title': '?????????????? ???? ??????????????????'
    }
    return render(request, 'shop/policies/pravila_na_koristenje.html', context)

def Cookies_Page(request):
    context = {
        'title': '???????????????? ???? ???????????????????? ?? ????????????????'
    }
    return render(request, 'shop/policies/politika_na_privatnost_i_kolacinja.html', context)


def export_excel(request):
    if request.method == 'POST':
        form = ExportOrder(request.POST)
        if form.is_valid():
            timezone = get_current_timezone()
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]
            total_ordered_dict = {}
            cart_offers_dict = {}
            thankyou_offers_dict = {}
            workbook = Workbook()
            worksheet = workbook.active
            row_num = 1
            
            worksheet.column_dimensions['A'].width = 20
            worksheet.column_dimensions['B'].width = 35
            worksheet.column_dimensions['C'].width = 35
            worksheet.column_dimensions['D'].width = 20
            worksheet.column_dimensions['E'].width = 20
            worksheet.column_dimensions['F'].width = 25
            worksheet.column_dimensions['G'].width = 10
            worksheet.column_dimensions['H'].width = 20
            worksheet.column_dimensions['I'].width = 65
            worksheet.column_dimensions['J'].width = 65
            worksheet.column_dimensions['K'].width = 10
            worksheet.column_dimensions['L'].width = 10
            worksheet.column_dimensions['M'].width = 100
            columns = ['DATA NA PORACKA', 'IME I PREZIME', 'ADRESA', 'GRAD', 'TELEFON', 'FEES', 'VKUPNO', 'DOSTAVA', 'IME NA PRODUKT', 'LABEL','KOLICINA', 'KOLICINA', '????????????????']
            for col_num in range(1, len(columns)+1):             
                cell =  worksheet.cell(row=row_num, column=col_num, value=columns[col_num - 1])

            rows = Order.objects.filter(Q(created_at__range = [date_from, date_to], status = 'Confirmed',) | Q(created_at__range = [date_from, date_to], status = 'Pending')).annotate(
                shippingann = Case(
                    When(shipping = True, then=Value('do vrata 130 den')),
                    When(shipping = False, then=Value('besplatna dostava'))
                ),
            ).order_by('-created_at').values_list('created_at', 'name', 'address', 'city', 'number', 'tracking_no', 'total_price', 'shippingann', 'number', 'number', 'number', 'number', 'message')
            print(rows)
            
            for row in rows:
                row_num += 1
                height = 10
                height2 = 10
                order_items = OrderItem.objects.filter(order__tracking_no = row[5]).annotate(full_product_title = Concat('product__title', Value(' '), 'attribute_name' ))
                order_fees = OrderFeesItem.objects.filter(order__tracking_no = row[5])
                order_items_total_name = ''
                order_items_total_label = ''
                order_fees_total = ''
                quantity = 0
                priority = False

                for fee in order_fees:
                    order_fees_total += str(fee.title) + '\n'
                    if(str(fee.title) == '?????????????????????? ??????????????'):
                        priority = True
                    height2 +=15
                    
                for item in order_items:
                    quantity += item.quantity
                    if item.label in total_ordered_dict:
                        total_ordered_dict[item.label] += item.quantity
                    else:
                        total_ordered_dict[item.label] = item.quantity
                        
                for item in order_items:
                    if item.is_cart_offer is True:
                        if item.label in cart_offers_dict:
                            cart_offers_dict[item.label] += item.quantity
                        else:
                            cart_offers_dict[item.label] = item.quantity

                    if item.is_thankyou_offer is True:
                        if item.label in thankyou_offers_dict:
                            thankyou_offers_dict[item.label] += item.quantity
                        else:
                            thankyou_offers_dict[item.label] = item.quantity
                            

                for item in order_items:
                    occurence = 0
                    
                    for item_check in order_items:
                        if item_check.full_product_title == item.full_product_title:
                            occurence += 1
                            if occurence > 1:
                                item_check.full_product_title = ''
                                item_check.label = ''

                    if item.full_product_title!='':
                        if priority is True:
                            order_items_total_name += 'PRIORITETNA ' + str(item.full_product_title) + ' x ' + str(item.quantity + occurence - 1) + '\n'
                            order_items_total_label += 'PRIORITETNA ' + str(item.label) + ' x ' + str(item.quantity + occurence - 1) + '\n'
                        else:
                            order_items_total_name += str(item.full_product_title) + ' x ' + str(item.quantity + occurence - 1) + '\n'
                            order_items_total_label += str(item.label) + ' x ' + str(item.quantity + occurence - 1) + '\n'
                        height += 15


                if(height2 > height):
                    height = height2

                worksheet.row_dimensions[row_num].height = height
                for col_num in range(1, len(row)+1):
                    worksheet.cell(row=row_num, column=col_num).alignment = Alignment(wrapText=True,  vertical='top')

                    if(col_num == 1):
                        date = row[col_num-1].astimezone(timezone)      
                        cell =  worksheet.cell(row=row_num, column=col_num).value = (date.strftime("%d.%m.%Y, %H:%M"))
                    elif(col_num == 6):
                        cell =  worksheet.cell(row=row_num, column=col_num).value = order_fees_total
                    elif(col_num == 9):
                        cell =  worksheet.cell(row=row_num, column=col_num).value = order_items_total_name
                    elif(col_num == 10):
                        cell =  worksheet.cell(row=row_num, column=col_num).value = order_items_total_label
                    elif(col_num == 11):
                        cell =  worksheet.cell(row=row_num, column=col_num).value = 'x' + str(quantity)
                    elif(col_num == 12):
                        cell =  worksheet.cell(row=row_num, column=col_num).value = quantity
                            
                    else:
                        cell =  worksheet.cell(row=row_num, column=col_num).value = str(row[col_num-1])

            print(total_ordered_dict)
            row_num += 4
            worksheet.cell(row=row_num, column=9).font = Font(bold=True)
            cell = worksheet.cell(row=row_num, column=9).value = 'VKUPNA KOLICINA'
            row_num += 1
            for key, value in total_ordered_dict.items():
                row_num += 1
                i = 0
                
                worksheet.cell(row=row_num, column=9).alignment = Alignment(wrapText=True,  vertical='top', horizontal='left')
                worksheet.cell(row=row_num, column=10).alignment = Alignment(wrapText=True,  vertical='top',horizontal='left')
                cell = worksheet.cell(row=row_num, column=9).value = str(key)
                cell = worksheet.cell(row=row_num, column = 10).value = value
                i += 1
            
            row_num += 2
            worksheet.cell(row=row_num, column=9).font = Font(bold=True)
            cell = worksheet.cell(row=row_num, column=9).value = 'PONUDI VO KOSNICKA'
            for key, value in cart_offers_dict.items():
                row_num += 1
                i = 0
                
                worksheet.cell(row=row_num, column=9).alignment = Alignment(wrapText=True,  vertical='top', horizontal='left')
                worksheet.cell(row=row_num, column=10).alignment = Alignment(wrapText=True,  vertical='top',horizontal='left')
                cell = worksheet.cell(row=row_num, column=9).value = str(key)
                cell = worksheet.cell(row=row_num, column = 10).value = value
                i += 1

            row_num += 2
            worksheet.cell(row=row_num, column=9).font = Font(bold=True)
            cell = worksheet.cell(row=row_num, column=9).value = 'THANKYOU PONUDI'
            for key, value in thankyou_offers_dict.items():
                row_num += 1
                i = 0
                
                worksheet.cell(row=row_num, column=9).alignment = Alignment(wrapText=True,  vertical='top', horizontal='left')
                worksheet.cell(row=row_num, column=10).alignment = Alignment(wrapText=True,  vertical='top',horizontal='left')
                cell = worksheet.cell(row=row_num, column=9).value = str(key)
                cell = worksheet.cell(row=row_num, column = 10).value = value
                i += 1

            response = HttpResponse(content=save_virtual_workbook(workbook))
            
            response['Content-Disposition'] = 'attachment; filename=eksport_' + str(date_from) + ' - ' + str(date_to) + '.xlsx'
            return response
    
    return redirect('/')
  
