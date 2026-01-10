from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(status="PUBLISHED")

    def lastmod(self, obj):
        return obj.date_posted


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            "dostava-page",
            "reklamacija-page",
            "rights-of-usage-page",
            "cookies-page",
        ]

    def location(self, item):
        return reverse(item)
