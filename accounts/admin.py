from django.contrib import admin

from .models import AISetting, ShopSetting, TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(AISetting)
class AISettingAdmin(admin.ModelAdmin):
    list_display = ("mode", "auto_call", "call_from", "call_until", "retries", "release_limit")


@admin.register(ShopSetting)
class ShopSettingAdmin(admin.ModelAdmin):
    list_display = ("shop_name", "currency", "phone")
