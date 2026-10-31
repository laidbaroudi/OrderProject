from django.contrib import admin

from .models import Call


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("order_no", "customer_name", "status", "duration_sec", "sentiment", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "order_no")
