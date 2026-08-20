from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DoctorProfile, PatientProfile, StaffProfile


# Register User model with custom admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login', 'last_login_ip', 'failed_login_attempts', 'locked_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Personal Information', {
            'fields': ('role', 'phone', 'date_of_birth', 'gender', 'address', 'profile_picture')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Hospital/Department', {
            'fields': ('hospital', 'department')
        }),
        ('Verification', {
            'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('HIPAA Compliance - Privacy', {
            'fields': ('privacy_consent_accepted', 'data_processing_consent', 'terms_accepted', 'terms_accepted_at'),
            'classes': ('collapse',)
        }),
        ('Security', {
            'fields': ('last_login_ip', 'failed_login_attempts', 'account_locked', 'locked_at'),
            'classes': ('collapse',)
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


# Register DoctorProfile model
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'experience_years', 'rating', 'created_at']
    list_filter = ['specialization', 'available_for_telemedicine', 'created_at']
    search_fields = ['user__username', 'user__email', 'license_number', 'qualification']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'license_number')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'qualification', 'experience_years', 'consultation_fee')
        }),
        ('Additional Information', {
            'fields': ('bio', 'available_for_telemedicine', 'languages')
        }),
        ('Rating', {
            'fields': ('rating', 'total_reviews')
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )


# Register PatientProfile model
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'insurance_provider', 'preferred_hospital', 'created_at']
    list_filter = ['blood_group', 'preferred_hospital', 'created_at']
    search_fields = ['user__username', 'user__email', 'insurance_provider', 'insurance_policy_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'blood_group')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'chronic_conditions', 'current_medications')
        }),
        ('Insurance', {
            'fields': ('insurance_provider', 'insurance_policy_number')
        }),
        ('Preferences', {
            'fields': ('preferred_hospital', 'preferred_doctor')
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )


# Register StaffProfile model
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'shift', 'hire_date', 'created_at']
    list_filter = ['shift', 'hire_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'employee_id', 'qualifications']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'hire_date')
        }),
        ('Work Details', {
            'fields': ('shift', 'qualifications', 'certifications')
        }),
        ('HIPAA Compliance - Soft Delete', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )
