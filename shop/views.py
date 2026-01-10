import csv
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone  # noqa
from django.utils.html import strip_tags
from django.views.generic import ListView

from .controller import facebook_pixel
from .forms import ExportOrder
from .models import *
from .services import OrderExcelExporter

# Create your views here.


def export_products_csv(request):
    products = Product.objects.all()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "ID",
            "Title",
            "Description",
            "Link",
            "Image Link",
            "Availability",
            "Price",
            "Condition",
            "Brand",
        ]
    )

    for product in products:
        content = strip_tags(product.content).replace("&nbsp;", "")
        content = os.linesep.join([s for s in content.splitlines() if s])
        if product.status == "VARIABLE":
            attributes = ProductAttribute.objects.filter(product=product)
            for attribute in attributes:
                attribute_name = ""
                if attribute.color is not None:
                    attribute_name = attribute.color.title

                if attribute.size is not None:
                    attribute_name = attribute.size.title

                if attribute.offer is not None:
                    attribute_name = attribute.offer.title

                writer.writerow(
                    [
                        str(product.id) + "_" + attribute.label,
                        product.title + " - " + attribute_name,
                        content,
                        "https://promotivno.com" + product.get_absolute_url(),
                        "https://promotivno.com" + product.thumbnail.url,
                        "in stock",
                        str(product.sale_price) + "MKD",
                        "New",
                        "PromotivnoMK",
                    ]
                )

        writer.writerow(
            [
                product.id,
                product.title,
                content,
                "https://promotivno.com" + product.get_absolute_url(),
                "https://promotivno.com" + product.thumbnail.url,
                "in stock",
                str(product.sale_price) + "MKD",
                "New",
                "PromotivnoMK",
            ]
        )

    return response


def ProductListView(request):
    products = Product.objects.filter(status__in=["PUBLISHED", "VARIABLE"]).order_by(
        "-date_posted"
    )
    paginator = Paginator(products, 16)
    page = request.GET.get("page")
    products = paginator.get_page(page)
    total = 0
    context = {
        "products": products,
        "title": "Почетна",
    }

    return render(request, "shop/home.html", context)


def CategoryView(request, slug):
    if Category.objects.filter(slug=slug):
        products = Product.objects.filter(category__slug=slug).order_by("-date_posted")
        paginator = Paginator(products, 16)
        page = request.GET.get("page")
        products = paginator.get_page(page)
        title = Category.objects.get(slug=slug).name

        context = {
            "products": products,
            "title": title,
        }

        return render(request, "shop/home.html", context)
    else:
        messages.warning(request, "Линкот што го следевте не постои")
        return redirect("shop-home")


def ProductView(request, slug):
    now = timezone.now()
    current_day = now.weekday()
    mapped_delivery_days = {
        0: ["Среда", "Петок"],
        1: ["Четврток", "Сабота"],
        2: ["Петок", "Понеделник"],
        3: ["Сабота", "Вторник"],
        4: ["Понеделник", "Среда"],
        5: ["Вторник", "Четврток"],
        6: ["Вторник", "Четврток"],
    }
    delivery_days = mapped_delivery_days[current_day]
    try:
        attributes = ProductAttribute.objects.filter(product__slug=slug)
        if attributes:
            for attribute in attributes:
                if attribute.is_disabled == False:
                    attribute.is_checked = True
                    default_attribute = attribute.checkattribute
                    break
        else:
            default_attribute = None

        gallery = ProductGallery.objects.filter(product__slug=slug)
        product = Product.objects.get(slug=slug)
        faq_toggle = ProductFAQ.objects.filter(product=product)
        if product.review_average != 0:
            reviews = Review.objects.filter(product__slug=slug)
        title = product.title
        percentage = 100 - int(product.sale_price / product.regular_price * 100)
        money_saved = product.regular_price - product.sale_price
        if product.status != "PRIVATE":
            try:
                facebook_pixel.ViewContentEvent(request, product)
            except:
                pass
            upsells = ProductUpsells.objects.filter(parent_product=product)
            if product.review_average != 0:
                count = reviews.count()

                context = {
                    "product": product,
                    "reviews": reviews,
                    "reviewcount": count,
                    "slider1": Product.objects.filter(category__name="ЗАЛИХА")[:8],
                    "slider2": Product.objects.filter(status="PUBLISHED")
                    .exclude(id=product.id)
                    .order_by("-date_posted")[:8],
                    "gallery": gallery,
                    "attributes": attributes,
                    "title": title,
                    "percentage": percentage,
                    "money_saved": money_saved,
                    "delivery_days": delivery_days,
                    "faq_toggle": faq_toggle,
                    "upsells": upsells,
                    "default_attribute": default_attribute,
                }
            else:
                context = {
                    "product": product,
                    "slider1": Product.objects.filter(category__name="ЗАЛИХА")[:8],
                    "slider2": Product.objects.filter(status="PUBLISHED")
                    .exclude(id=product.id)
                    .order_by("-date_posted")[:8],
                    "attributes": attributes,
                    "gallery": gallery,
                    "title": title,
                    "percentage": percentage,
                    "money_saved": money_saved,
                    "delivery_days": delivery_days,
                    "faq_toggle": faq_toggle,
                    "upsells": upsells,
                    "default_attribute": default_attribute,
                }

            return render(request, "shop/product-page.html", context)
        else:
            return redirect("shop-home")
    except:
        messages.warning(request, "Линкот што го следевте не постои")
        return redirect("shop-home")


def CheckoutView(request):
    orderFees = CheckoutFees.objects.all()
    try:
        facebook_pixel.InitiateCheckoutEvent(request)
    except:
        pass
    try:
        cartFees = CartFees.objects.filter(cart__session=request.session["nonuser"])
    except:
        cartFees = None

    feetotal = 0
    for orderfee in orderFees:
        for cartfee in cartFees or []:
            if orderfee == cartfee.fee:
                orderfee.is_added = True
                feetotal += cartfee.price

    context = {
        "title": "Кон Нарачка",
        "orderFees": orderFees,
        "cartFees": cartFees,
        "feetotal": feetotal,
    }

    return render(request, "shop/checkout.html", context)


def ThankYouView(request, slug):
    order = get_object_or_404(Order, tracking_no=slug)
    name = order.name.split(" ")[0]
    orderItems = OrderItem.objects.filter(order__tracking_no=slug)  # Sql join ?
    orderItems.reverse()
    offerproduct = OrderItem.objects.filter(
        order__tracking_no=slug, is_cart_offer=False, is_upsell_offer=False
    ).first()
    if offerproduct is not None:
        if offerproduct.attribute_price is not None:
            offerproduct.attribute_price = (
                offerproduct.attribute_price - offerproduct.attribute_price * 20 // 100
            )
        else:
            offerproduct.price = offerproduct.price - offerproduct.price * 20 // 100
    orderFees = OrderFeesItem.objects.filter(order__tracking_no=slug)
    feetotal = 0
    for fee in orderFees:
        feetotal += fee.price

    title = "Ви благодариме!"
    context = {
        "order": order,
        "orderItems": orderItems,
        "offerproduct": offerproduct,
        "orderFees": orderFees,
        "feetotal": feetotal,
        "title": title,
        "name": name,
    }

    return render(request, "shop/thank-you.html", context)


class SearchResultsView(ListView):
    model = Product
    template_name = "shop/home.html"
    extra_context = {
        "title": "Барање",
    }
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(
            Q(title__icontains=query, status__in=["PUBLISHED", "VARIABLE"])
            | Q(sku__icontains=query, status__in=["PUBLISHED", "VARIABLE"])
        )

        return object_list


def login_shopmanager(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("shopmanagerhome")
    else:
        context = {
            "title": "Login",
        }
        if request.method == "POST":
            name = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("shopmanagerhome")
            else:
                messages.error(request, "Invalid username or Password")
                return redirect("/")
        return render(request, "shop/shopmanager/login.html", context)


def logout_shopmanager(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")

    return redirect("/")


@login_required(login_url="/shopmanager/login")
def shopmanager_dashboard(request):
    orders = (
        Order.objects.filter(status="Pending")
        .prefetch_related("order")
        .order_by("-id")[:50]
    )
    orderfees = OrderFeesItem.objects.filter(order__status="Pending").order_by("-id")
    title = "НЕПОТВРДЕНИ НАРАЧКИ"
    form = ExportOrder()
    context = {
        "orders": orders,
        "orderFees": orderfees,
        "heading": title,
        "order_status": "Непотврдена",
        "form": form,
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


@login_required(login_url="/shopmanager/login")
def shopmanager_confirmed(request):
    orders = (
        Order.objects.filter(status="Confirmed")
        .prefetch_related("order")
        .order_by("-updated_at")[:50]
    )
    orderfees = OrderFeesItem.objects.filter(order__status="Confirmed").order_by("-id")
    title = "ПОТВРДЕНИ НАРАЧКИ"
    context = {
        "orders": orders,
        "orderFees": orderfees,
        "heading": title,
        "order_status": "Потврдена",
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


@login_required(login_url="/shopmanager/login")
def shopmanager_abandoned_carts(request):
    abandoned_carts = AbandonedCarts.objects.all().order_by("-id")
    abandoned_cartItems = AbandonedCarts.objects.all().order_by("-id")
    paginator = Paginator(abandoned_carts, 50)
    page = request.GET.get("page")
    carts = paginator.get_page(page)
    # print(abandoned_carts.first().get_items)
    context = {
        "carts": carts,
        "cartItems": abandoned_cartItems,
        "title": "Abandoned Carts",
    }
    return render(request, "shop/shopmanager/abandoned_carts.html", context)


@login_required(login_url="/shopmanager/login")
def shopmanager_deleted(request):
    orders = (
        Order.objects.filter(status="Deleted")
        .prefetch_related("order")
        .order_by("-updated_at")[:50]
    )
    orderfees = OrderFeesItem.objects.filter(order__status="Deleted").order_by("-id")
    title = "ИЗБРИШЕНИ НАРАЧКИ"
    context = {
        "orders": orders,
        "orderFees": orderfees,
        "heading": title,
        "order_status": "Избришена",
    }
    return render(request, "shop/shopmanager/dashboard.html", context)


@login_required(login_url="/shopmanager/login")
def shopmanager_create_order(request):
    context = {"heading": "Креири нарачка"}

    return render(request, "shop/shopmanager/create_order.html", context)


def Dostava(request):
    context = {"title": "Политика за достава"}
    return render(request, "shop/policies/dostava.html", context)


def Reklamacija(request):
    context = {"title": "Политика за рекламација"}
    return render(request, "shop/policies/reklamacija.html", context)


def Pravila_Na_Koristenje(request):
    context = {"title": "Правила на користење"}
    return render(request, "shop/policies/pravila_na_koristenje.html", context)


def Cookies_Page(request):
    context = {"title": "Политика за приватност и колачиња"}
    return render(
        request, "shop/policies/politika_na_privatnost_i_kolacinja.html", context
    )


def export_excel(request):
    if request.method == "POST":
        form = ExportOrder(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]

            # Generate
            exporter = OrderExcelExporter(date_from, date_to)
            workbook = exporter.generate()

            # Return File
            output = BytesIO()
            workbook.save(output)
            output.seek(0)

            filename = f"eksport_{date_from} - {date_to}.xlsx"
            response = HttpResponse(
                content=output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response

    return redirect("/")


def get_recent_ordered(request):
    if request.method == "GET":
        random_int = randint(1, 20)
        product = Product.objects.order_by("-pk").filter(status="PUBLISHED")[random_int]
        thumbnail = product.thumbnail_loop_as_jpeg.url
        if "image/webp" in request.META.get("HTTP_ACCEPT", ""):
            thumbnail = product.thumbnail_loop.url
        return JsonResponse(
            {
                "url": product.get_absolute_url(),
                "thumbnail": thumbnail,
                "title": product.title,
                "regular_price": product.regular_price,
                "sale_price": product.sale_price,
            }
        )
    else:
        return redirect("/")


def create_or_check_abandoned_cart(request):
    if request.method == "POST":
        current_cart = Cart.objects.get(session=request.session["nonuser"])
        current_cartitems = CartItems.objects.filter(cart=current_cart)

        if current_cartitems.count() == 0:
            return JsonResponse({"status": "No cartItems"})

        else:
            abandoned_name = str(request.POST.get("name"))
            abandoned_phone_number = str(request.POST.get("phone"))
            abandoned_address = str(request.POST.get("address"))
            # abandoned_cart = Abandoned_Carts.objects.update_or_create(session = request.session['nonuser'], defaults={
            #     'name': abandoned_name,
            #     'phone': abandoned_phone_number
            # })

            try:
                abandoned_cart = AbandonedCarts.objects.get(
                    session=request.session["nonuser"]
                )
                abandoned_cart.name = abandoned_name
                abandoned_cart.phone = abandoned_phone_number
                abandoned_cart.address = abandoned_address
                abandoned_cart.save()
                print("Found and updated")
            except:
                abandoned_cart = AbandonedCarts.objects.create(
                    session=request.session["nonuser"]
                )
                abandoned_cart.name = abandoned_name
                abandoned_cart.phone = abandoned_phone_number
                abandoned_cart.address = abandoned_address
                abandoned_cart.save()
                print("Not Found and created")
            print(abandoned_cart)

            for current_item in current_cartitems:
                abandoned_item = AbandonedCartItems.objects.filter(
                    cart=abandoned_cart,
                    product=current_item.product,
                    attributename=current_item.attributename,
                    product_qty=current_item.product_qty,
                    attribute=current_item.attribute,
                    attributeprice=current_item.attributeprice,
                    offer_price=current_item.offer_price,
                ).first()
                print("Abandoned item: ", abandoned_item)
                if not abandoned_item:
                    AbandonedCartItems.objects.create(
                        cart=abandoned_cart,
                        product=current_item.product,
                        attributename=current_item.attributename,
                        product_qty=current_item.product_qty,
                        attribute=current_item.attribute,
                        attributeprice=current_item.attributeprice,
                        offer_price=current_item.offer_price,
                    )

        return JsonResponse({"status": "Success"})
    else:
        return redirect("/")


def remove_abandoned_cart(request):
    if request.method == "POST":
        id = str(request.POST.get("cartId"))
        AbandonedCarts.objects.get(pk=id).delete()
        return JsonResponse({"status": "Success"})
    else:
        return redirect("/")


def call_pixel_checkout(request):
    try:
        facebook_pixel.InitiateCheckoutEvent(request)
        return JsonResponse({"status": "Success"})
    except:
        return JsonResponse({"status": "error"})


def get_checkout_offer_status(request):
    if request.method == "POST":
        try:
            current_cart = Cart.objects.get(session=request.session["nonuser"])
            print(current_cart)
            offer_status = current_cart.has_viewed_checkout_offer
            if offer_status == True:
                return JsonResponse({"status": "True"})
            else:
                current_cart.has_viewed_checkout_offer = True
                current_cart.has_viewed_checkout_offer_time = timezone.now()
                current_cart.save()
                return JsonResponse({"status": "False"})
        except:
            return JsonResponse({"status": "Cart not found"}, status=400)
    else:
        print("ahh")
        return JsonResponse({"status": "Bad Request.."}, status=400)


def accept_checkout_offer(request):
    if request.method == "POST":
        try:
            current_cart = Cart.objects.get(session=request.session["nonuser"])
            current_cart.has_accepted_checkout_offer = True
            current_cart.save()
            cart_priority_fee = CartFees.objects.filter(
                cart=current_cart, fee_id=7
            ).first()
            if cart_priority_fee:
                cart_priority_fee.delete()

            CartFees.objects.create(
                cart=current_cart,
                fee_id=7,
                title="Бесплатна приоритетна достава",
                price=0,
                is_free=True,
            )
            return JsonResponse({"status": "Success"})
        except:
            return JsonResponse({"status": "Cart not found"}, status=400)

    else:
        return JsonResponse({"status": "Bad Request.."}, status=400)


def change_offer_checkout_qty(request):
    if request.method == "POST":
        orderItem_id = int(request.POST.get("orderItem_id"))
        item = OrderItem.objects.filter(pk=orderItem_id).first()

        if item:
            order = item.order
            subtotal = order.subtotal_price - item.get_product_total
            total = order.total_price - item.get_product_total

            item.quantity = int(request.POST.get("quantity"))
            item.save()
            order.subtotal_price = subtotal + item.get_product_total
            order.total_price = total + item.get_product_total
            order.save()
            return JsonResponse({"status": "Success"})
        else:
            return JsonResponse({"status": "Bad Request.."}, status=400)

    else:
        return JsonResponse({"status": "Bad Request.."}, status=400)
