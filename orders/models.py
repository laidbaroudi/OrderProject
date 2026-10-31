from django.conf import settings
from django.db import models


class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CALLING = "calling", "Calling"
        APPROVAL = "approval", "Awaiting approval"
        PACKING = "packing", "Sent to packing"
        CANCELLED = "cancelled", "Cancelled"
        ESCALATED = "escalated", "Escalated"

    class Source(models.TextChoices):
        SHOPIFY = "Shopify", "Shopify"
        WHATSAPP = "WhatsApp", "WhatsApp"
        WEBSITE = "Website", "Website"

    order_no = models.PositiveIntegerField(unique=True)
    customer_name = models.CharField(max_length=200)
    customer = models.ForeignKey(
        "customers.Customer", null=True, blank=True, on_delete=models.SET_NULL, related_name="orders"
    )
    product = models.ForeignKey(
        "products.Product", null=True, blank=True, on_delete=models.SET_NULL, related_name="orders"
    )
    item_name = models.CharField(max_length=200, blank=True, default="")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.SHOPIFY)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.CharField(max_length=200, blank=True, default="")
    release_note = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-order_no"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"#{self.order_no} - {self.customer_name} ({self.status})"
