from django.contrib import admin
from .models import StegoOperation

# Register your models here.

@admin.register(StegoOperation)
class StegoOperationAdmin(admin.ModelAdmin):
    list_display = ('user', 'operation_type', 'status', 'created_at')
    list_filter = ('operation_type', 'status', 'created_at')
    search_fields = ('user__username', 'original_filename')
    readonly_fields = ('created_at', 'ip_address')
    fieldsets = (
        ('Operation Details', {
            'fields': ('user', 'operation_type', 'original_filename', 'message_length')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address'),
            'classes': ('collapse',)
        }),
    )