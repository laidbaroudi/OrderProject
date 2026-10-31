from django.conf import settings
from django.db import models


class FitCheck(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fit_checks", null=True, blank=True)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="fit_checks")
    score = models.PositiveIntegerField(default=0)
    verdict = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Fit Check"
        verbose_name_plural = "Fit Checks"

    def __str__(self):
        return f"FitCheck {self.product_id}: {self.score}"
