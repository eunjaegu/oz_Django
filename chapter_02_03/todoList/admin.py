from django.contrib import admin

# todo > admin.py

from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_complete', 'start_date', 'end_date')
    list_filter = ('is_complete',)
    search_fields = ('title',)
    ordering = ('start_date',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_complete')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )


