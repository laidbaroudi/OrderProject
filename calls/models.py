from django.conf import settings
from django.db import models


class Call(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="calls", null=True, blank=True)
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        UNREACHABLE = "unreachable", "Unreachable"
        DECLINED = "declined", "Declined"
        ESCALATED = "escalated", "Escalated"

    order = models.ForeignKey(
        "orders.Order", null=True, blank=True, on_delete=models.SET_NULL, related_name="calls"
    )
    customer_name = models.CharField(max_length=200)
    order_no = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)
    duration_sec = models.PositiveIntegerField(default=0)
    sentiment = models.FloatField(null=True, blank=True)
    transcript = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Call"
        verbose_name_plural = "Calls"

    def __str__(self):
        return f"Call #{self.order_no} with {self.customer_name} ({self.status})"
