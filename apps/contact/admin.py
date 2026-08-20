from django.contrib import admin
from .models import ContactMessage, NewsletterSubscription


# Register ContactMessage model
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'subject', 'status', 'created_at']
    list_filter = ['inquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status Tracking', {
            'fields': ('status', 'responded_at', 'response_notes')
        }),
        ('HIPAA Compliance - Privacy', {
            'fields': ('privacy_consent', 'data_processing_consent', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )


# Register NewsletterSubscription model
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'receive_updates', 'receive_promotions', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'ip_address']
    
    fieldsets = (
        ('Subscription Information', {
            'fields': ('email', 'name', 'is_active')
        }),
        ('Subscription Status', {
            'fields': ('subscribed_at', 'unsubscribed_at')
        }),
        ('Preferences', {
            'fields': ('receive_updates', 'receive_promotions')
        }),
        ('HIPAA Compliance - Privacy', {
            'fields': ('privacy_consent', 'marketing_consent', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )
