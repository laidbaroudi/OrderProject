from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_no", "customer_name", "item_name", "total_price", "status", "source", "created_at")
    list_filter = ("status", "source")
    search_fields = ("customer_name", "item_name", "order_no")
