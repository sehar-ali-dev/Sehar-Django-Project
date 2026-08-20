from django.contrib import admin
from .models import Hospital, Department, Specialization


# Register Hospital model
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'license_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'phone', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'license_number')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )


# Register Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital', 'location', 'is_active', 'created_at']
    list_filter = ['hospital', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('hospital', 'name', 'location')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )


# Register Specialization model
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'icon')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )
