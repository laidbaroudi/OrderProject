from django.conf import settings
from django.db import models


class Challenge(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challenges", null=True, blank=True)
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        LIVE = "live", "Live"
        DONE = "done", "Done"

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="challenges")
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    entry_fee = models.PositiveIntegerField(default=50)
    winner_name = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

    def __str__(self):
        return f"Challenge: {self.product.name} ({self.status})"


class Entry(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="entries")
    player_name = models.CharField(max_length=200)
    game = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Challenge Entry"
        verbose_name_plural = "Challenge Entries"

    def __str__(self):
        return f"{self.player_name} -> {self.challenge_id} ({self.game})"
