from django.conf import settings
from django.db import models


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, default="")
    price = models.PositiveIntegerField(help_text="Price in DZD")
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    sku = models.CharField(max_length=50, unique=True)
    sold_30d = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    ai_added = models.BooleanField(default=False)
    garment_chest_cm = models.PositiveIntegerField(null=True, blank=True)
    garment_waist_cm = models.PositiveIntegerField(null=True, blank=True)
    follow = models.BooleanField(default=False)
    expected_restock = models.DateField(null=True, blank=True)
    supplier_note = models.TextField(blank=True, default="")
    verified_buyers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def stock_status(self):
        if self.stock <= 0:
            return "out"
        if self.stock <= self.low_stock_threshold:
            return "low"
        return "in"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="products/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Photo for {self.product.name}"
