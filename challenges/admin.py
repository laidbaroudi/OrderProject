from django.contrib import admin

from .models import Challenge, Entry


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("product", "status", "entry_fee", "winner_name", "created_at")
    list_filter = ("status",)
    inlines = [EntryInline]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("challenge", "player_name", "game")
