from django.contrib import admin
from .models import ServiceCategory, Service


# Register ServiceCategory model
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


# Register Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_minutes', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'short_description', 'detailed_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Service Details', {
            'fields': ('short_description', 'detailed_description', 'service_image')
        }),
        ('Pricing and Duration', {
            'fields': ('price', 'duration_minutes')
        }),
        ('Availability', {
            'fields': ('status', 'is_featured')
        }),
        ('SEO Fields', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('requirements', 'what_to_expect'),
            'classes': ('collapse',)
        }),
        ('HIPAA Compliance', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )
