from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'created_at')  # Что отображать в списке записей
    search_fields = ('title', 'content')                      # Поисковые поля
    list_filter = ('user', 'subject', 'created_at')           # Фильтры слева
    readonly_fields = ('created_at', 'updated_at')