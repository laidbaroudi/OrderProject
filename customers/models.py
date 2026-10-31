from django.conf import settings
from django.db import models


class Customer(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customers", null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True, default="")
    address = models.CharField(max_length=300, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="", help_text="Wilaya")

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name
