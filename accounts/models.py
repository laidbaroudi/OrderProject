from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        SELLER = "seller", "Seller"
        CUSTOMER = "customer", "Customer"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    full_name = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.user.email} ({self.role})"


class TeamMember(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_members", null=True, blank=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"


class AISetting(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_settings", null=True, blank=True)
    class Mode(models.TextChoices):
        OWNER = "owner", "Owner"
        AI = "ai", "AI"

    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.OWNER)
    auto_call = models.BooleanField(default=True)
    call_from = models.CharField(max_length=5, default="09:00")
    call_until = models.CharField(max_length=5, default="20:00")
    retries = models.PositiveIntegerField(default=2)
    voice = models.CharField(max_length=100, default="Sarah (FR)")
    opening_line = models.TextField(blank=True, default="")
    shop_notes = models.TextField(blank=True, default="")
    release_limit = models.PositiveIntegerField(default=10000)

    class Meta:
        verbose_name = "AI Setting"
        verbose_name_plural = "AI Settings"

    def __str__(self):
        return f"AI settings ({self.mode})"


class ShopSetting(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shop_settings", null=True, blank=True)
    shop_name = models.CharField(max_length=200, default="TechZone")
    currency = models.CharField(max_length=10, default="DZD")
    phone = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        verbose_name = "Shop Setting"
        verbose_name_plural = "Shop Settings"

    def __str__(self):
        return self.shop_name
