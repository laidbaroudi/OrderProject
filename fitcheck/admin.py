from django.contrib import admin

from .models import FitCheck


@admin.register(FitCheck)
class FitCheckAdmin(admin.ModelAdmin):
    list_display = ("product", "score", "verdict", "created_at")
