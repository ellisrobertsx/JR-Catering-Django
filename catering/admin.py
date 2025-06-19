from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import FoodItem, DrinkItem, Booking, Contact

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(DrinkItem)
class DrinkItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date', 'time', 'guests', 'status', 'created_at', 'admin_response_preview')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('name', 'email', 'phone', 'user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'name', 'email', 'phone', 'date', 'time', 'guests', 'special_requests')
        }),
        ('Admin Management', {
            'fields': ('status', 'admin_response', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def admin_response_preview(self, obj):
        if obj.admin_response:
            return obj.admin_response[:50] + "..." if len(obj.admin_response) > 50 else obj.admin_response
        return "No response"
    admin_response_preview.short_description = "Admin Response"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        if change and 'admin_response' in form.changed_data:
            # You could add email notification here if needed
            pass
        super().save_model(request, obj, form, change)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at', 'message_preview')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def message_preview(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
    message_preview.short_description = "Message Preview"
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"