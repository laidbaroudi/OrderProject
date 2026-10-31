from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "stock", "stock_status", "sold_30d")
    list_filter = ("category", "ai_added", "verified_buyers")
    search_fields = ("name", "sku")
