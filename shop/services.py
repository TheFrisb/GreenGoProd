import mimetypes
import os
import re  # <--- NEW IMPORT
from collections import defaultdict
from datetime import timedelta

import openpyxl
from django.db.models import Case, CharField, Prefetch, Q, Value, When
from django.utils import timezone as django_timezone
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# Import your models
from .models import Order, OrderItem

mimetypes.add_type("image/webp", ".webp")


class OrderExcelExporter:
    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to
        self.timezone = django_timezone.get_current_timezone()

        self.wb = Workbook()
        self.ws = self.wb.active
        self.row_num = 1

        self.total_ordered_dict = defaultdict(int)
        self.total_ordered_stock_price = {}
        self.cart_offers_dict = defaultdict(int)
        self.upsell_offers_dict = defaultdict(int)
        self.thankyou_offers_dict = defaultdict(int)
        self.fee_offers_dict = defaultdict(int)

        self.thin_border = Side(border_style="thin", color="151515")
        self.border_all = Border(
            left=self.thin_border,
            right=self.thin_border,
            top=self.thin_border,
            bottom=self.thin_border,
        )
        self.header_font = Font(bold=True)

    def _get_stock_multiplier(self, text):
        """
        Parses text for pattern 'X [number]' (case insensitive).
        Example: 'Pack X 2' returns 2. 'Blue' returns 1.
        """
        if not text:
            return 1
        # Regex: Look for X followed by one or more spaces, then digits
        match = re.search(r"[xX]\s+(\d+)", text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return 1
        return 1

    def generate(self):
        self._setup_main_sheet()
        orders, duplicate_orders = self._get_orders_and_duplicates()

        for order in orders:
            self._write_order_row(order)

        self.row_num += 2
        self._write_duplicates_section(duplicate_orders)

        self.row_num += 4
        self._write_summaries()

        self._generate_procurement_sheet()

        return self.wb

    def _setup_main_sheet(self):
        widths = [20, 35, 35, 20, 20, 25, 10, 20, 65, 65, 10, 10, 100]
        columns = [
            "DATA NA PORACKA",
            "IME I PREZIME",
            "ADRESA",
            "GRAD",
            "TELEFON",
            "FEES",
            "VKUPNO",
            "DOSTAVA",
            "IME NA PRODUKT",
            "LABEL",
            "KOLICINA",
            "KOLICINA",
            "КОМЕНТАР",
        ]

        for i, width in enumerate(widths, 1):
            self.ws.column_dimensions[get_column_letter(i)].width = width
            self.ws.cell(row=self.row_num, column=i, value=columns[i - 1])

    def _get_orders_and_duplicates(self):
        base_qs = (
            Order.objects.filter(status__in=["Confirmed", "Pending"])
            .annotate(
                shippingann=Case(
                    When(shipping=True, then=Value("do vrata 180 den")),
                    When(shipping=False, then=Value("besplatna dostava")),
                    output_field=CharField(),
                )
            )
            .select_related()
            .prefetch_related(
                Prefetch(
                    "order",
                    queryset=OrderItem.objects.select_related(
                        "product", "product__supplier"
                    ),
                ),
                "orderfeesitem_set",
            )
            .order_by("-created_at")
        )

        current_orders = list(
            base_qs.filter(created_at__range=[self.date_from, self.date_to])
        )

        date_from_week_before = self.date_from - timedelta(days=7)
        lookback_orders = list(
            base_qs.filter(created_at__range=[date_from_week_before, self.date_from])
        )

        duplicate_orders = []
        seen_tracking_ids = set()

        def get_skus(ord_obj):
            return {item.product.sku for item in ord_obj.order.all()}

        def add_dup(ord_obj):
            if ord_obj.tracking_no not in seen_tracking_ids:
                seen_tracking_ids.add(ord_obj.tracking_no)
                duplicate_orders.append(ord_obj)

        for i, order_a in enumerate(current_orders):
            skus_a = get_skus(order_a)
            for order_b in current_orders[i + 1 :]:
                if order_a.name == order_b.name or order_a.number == order_b.number:
                    skus_b = get_skus(order_b)
                    if not skus_a.isdisjoint(skus_b):
                        add_dup(order_a)
                        add_dup(order_b)
            for order_b in lookback_orders:
                if order_a.name == order_b.name or order_a.number == order_b.number:
                    skus_b = get_skus(order_b)
                    if not skus_a.isdisjoint(skus_b):
                        add_dup(order_a)
                        add_dup(order_b)

        return current_orders, duplicate_orders

    def _write_order_row(self, order):
        self.row_num += 1
        order_items = order.order.all()
        order_fees = order.orderfeesitem_set.all()

        fees_text = ""
        items_name_text = ""
        items_label_text = ""
        total_quantity = 0
        is_priority = False

        for fee in order_fees:
            fees_text += f"{fee.title}\n"
            self.fee_offers_dict[str(fee.title)] += 1
            if str(fee.title) in [
                "Приоритетна достава",
                "Приоритетна Достава + Осигурување на Пакет",
                "Бесплатна приоритетна достава",
            ]:
                is_priority = True

        processed_items_list = []
        for item in order_items:
            full_title = item.product.title
            if item.attribute_name:
                full_title += f" {item.attribute_name}"

            processed_items_list.append((full_title, item))
            self.total_ordered_dict[full_title] += item.quantity

            # --- STOCK PRICE LOGIC (SHEET 1) ---
            multiplier = self._get_stock_multiplier(full_title)
            base_price = item.product.supplier_stock_price or 0
            self.total_ordered_stock_price[full_title] = base_price * multiplier
            # -----------------------------------

            if item.is_cart_offer:
                if item.is_upsell_offer:
                    self.upsell_offers_dict[item.label] += item.quantity
                else:
                    self.cart_offers_dict[item.label] += item.quantity
            if item.is_thankyou_offer:
                self.thankyou_offers_dict[item.label] += item.quantity

            total_quantity += item.quantity

        written_titles = set()
        for full_title, item in processed_items_list:
            if full_title in written_titles:
                continue
            count = sum(1 for t, i in processed_items_list if t == full_title)
            qty_display = item.quantity + count - 1
            prefix = "PRIORITETNA " if is_priority else ""
            lbl = item.label if item.label else ""
            items_name_text += f"{prefix}{full_title} x {qty_display}"
            items_label_text += f"{prefix}{lbl} x {qty_display}"
            written_titles.add(full_title)

        height = 10 + (len(written_titles) * 15)
        self.ws.row_dimensions[self.row_num].height = height

        def w(col, val):
            c = self.ws.cell(row=self.row_num, column=col, value=val)
            c.alignment = Alignment(wrapText=True, vertical="top")

        date_str = order.created_at.astimezone(self.timezone).strftime(
            "%d.%m.%Y, %H:%M"
        )
        w(1, date_str)
        w(2, order.name)
        w(3, order.address)
        w(4, order.city)
        w(5, order.number)
        w(6, fees_text)
        w(7, order.total_price)
        w(8, order.shippingann)
        w(9, items_name_text)
        w(10, items_label_text)
        w(11, f"x{total_quantity}")
        w(12, total_quantity)
        w(13, order.message)

    def _write_duplicates_section(self, duplicate_orders):
        cell = self.ws.cell(
            row=self.row_num,
            column=2,
            value="DUPLI NARACKI" if duplicate_orders else "NEMA DUPLI NARACKI",
        )
        cell.font = self.header_font
        if duplicate_orders:
            for order in duplicate_orders:
                self._write_order_row(order)

    def _write_summaries(self):
        def write_table(title, data_dict, include_price=False):
            self.ws.cell(row=self.row_num, column=9, value=title).font = (
                self.header_font
            )
            self.row_num += 1
            for key, value in data_dict.items():
                self.row_num += 1
                align = Alignment(wrapText=True, vertical="top", horizontal="left")
                c1 = self.ws.cell(row=self.row_num, column=9, value=str(key))
                c1.alignment = align
                c2 = self.ws.cell(row=self.row_num, column=10, value=value)
                c2.alignment = align
                if include_price:
                    c3 = self.ws.cell(
                        row=self.row_num,
                        column=11,
                        value=self.total_ordered_stock_price.get(key),
                    )
                    c3.alignment = align
            self.row_num += 2

        write_table("VKUPNA KOLICINA", self.total_ordered_dict, include_price=True)
        write_table("PONUDI VO KOSNICKA", self.cart_offers_dict)
        write_table("PONUDI NA PRODUCT PAGE", self.upsell_offers_dict)
        write_table("THANKYOU PONUDI", self.thankyou_offers_dict)
        write_table("CHECKOUT FEES", self.fee_offers_dict)

    def _generate_procurement_sheet(self):
        ws2 = self.wb.create_sheet("Nabavki")
        ws2.column_dimensions["A"].width = 20.3
        ws2.column_dimensions["B"].width = 30

        items = OrderItem.objects.filter(
            Q(order__created_at__range=[self.date_from, self.date_to]),
            Q(order__status__in=["Confirmed", "Pending"]),
        ).select_related("product", "product__supplier")

        grouped_data = defaultdict(lambda: defaultdict(lambda: {"qty": 0, "obj": None}))

        for item in items:
            supplier_name = item.product.supplier.name
            if item.attribute_name:
                label = f"{item.product.title} {item.attribute_name}"
            else:
                label = item.product.title

            entry = grouped_data[supplier_name][label]
            entry["qty"] += item.quantity
            if entry["obj"] is None:
                entry["obj"] = item

        sorted_suppliers = sorted(grouped_data.keys())
        row_num = 1

        for supplier_name in sorted_suppliers:
            ws2.row_dimensions[row_num].height = 30
            ws2.merge_cells(f"A{row_num}:E{row_num}")
            header = ws2.cell(row=row_num, column=1, value=supplier_name)
            header.font = Font(bold=True, size=24)
            header.alignment = Alignment(horizontal="center", vertical="center")
            for col in range(1, 6):
                ws2.cell(row=row_num, column=col).border = self.border_all

            row_num += 1
            start_row = row_num
            supplier_products = grouped_data[supplier_name]

            for label, data in supplier_products.items():
                qty = data["qty"]
                item_obj = data["obj"]
                product = item_obj.product

                ws2.row_dimensions[row_num].height = 113.5

                # Image (PNG)
                try:
                    if product.thumbnail:
                        image_path = product.export_image.path
                        if os.path.exists(image_path):
                            img = openpyxl.drawing.image.Image(image_path)
                            img.width = 150
                            img.height = 150
                            ws2.add_image(img, f"A{row_num}")
                except Exception as e:
                    print(f"Export Image Error for {label}: {e}")

                def cell(c, v, bold=False, fill=None):
                    cl = ws2.cell(row=row_num, column=c, value=v)
                    cl.alignment = Alignment(
                        wrapText=True, horizontal="center", vertical="center"
                    )
                    cl.border = self.border_all
                    if bold:
                        cl.font = Font(bold=True)
                    if fill:
                        cl.fill = fill
                    return cl

                # --- STOCK PRICE LOGIC (SHEET 2) ---
                multiplier = self._get_stock_multiplier(label)
                base_price = product.supplier_stock_price or 0
                final_stock_price = base_price * multiplier
                # -----------------------------------

                cell(1, "")
                cell(2, label)
                cell(3, qty)
                cell(4, final_stock_price)  # Updated
                cell(5, f"=PRODUCT(C{row_num},D{row_num})")

                row_num += 1

            end_row = row_num
            yellow = PatternFill(
                start_color="FFFF00", end_color="FFFF00", patternType="solid"
            )

            sum_range_end = row_num - 1
            if sum_range_end >= start_row:
                total_cell = ws2.cell(
                    row=row_num, column=4, value=f"=SUM(E{start_row}:E{sum_range_end})"
                )
                total_cell.alignment = Alignment(horizontal="center", vertical="center")
                total_cell.border = self.border_all
                total_cell.font = Font(bold=True)
                total_cell.fill = yellow

            row_num += 3
