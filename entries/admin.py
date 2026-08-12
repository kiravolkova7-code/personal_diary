from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "subject", "created_at")
    search_fields = ("title", "content")
    list_filter = ("user", "subject", "created_at")
    readonly_fields = ("created_at", "updated_at")
