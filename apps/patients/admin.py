from django.contrib import admin
from .models import MedicalHistory, MedicalRecord, PatientDocument, InsuranceInformation


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for MedicalHistory model.
    Provides filtering and search for mental health conditions.
    """
    list_display = ['patient', 'condition_name', 'diagnosis_date', 'status', 'created_at']
    list_filter = ['status', 'diagnosis_date', 'created_at']
    search_fields = ['patient__username', 'patient__email', 'condition_name', 'therapy_history']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Condition Details', {
            'fields': ('condition_name', 'diagnosis_date', 'status')
        }),
        ('Treatment Information', {
            'fields': ('therapy_history', 'current_medications', 'notes')
        }),
        ('HIPAA Compliance', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for MedicalRecord model.
    Tracks therapy sessions and medical visits.
    """
    list_display = ['patient', 'doctor_name', 'visit_date', 'mental_health_diagnosis', 'created_at']
    list_filter = ['visit_date', 'created_at']
    search_fields = ['patient__username', 'doctor_name', 'mental_health_diagnosis', 'therapy_notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('patient', 'doctor_name', 'visit_date')
        }),
        ('Clinical Details', {
            'fields': ('mental_health_diagnosis', 'therapy_notes', 'prescription_details', 'recommended_treatment_plan')
        }),
        ('HIPAA Compliance', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    """
    Admin interface for PatientDocument model.
    Manages psychological assessments and medical documents.
    """
    list_display = ['patient', 'document_title', 'document_type', 'uploaded_at', 'created_at']
    list_filter = ['document_type', 'uploaded_at', 'created_at']
    search_fields = ['patient__username', 'document_title', 'notes']
    readonly_fields = ['uploaded_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('patient', 'document_title', 'document_type', 'file')
        }),
        ('Additional Details', {
            'fields': ('uploaded_at', 'notes')
        }),
        ('HIPAA Compliance', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InsuranceInformation)
class InsuranceInformationAdmin(admin.ModelAdmin):
    """
    Admin interface for InsuranceInformation model.
    Manages mental health insurance coverage details.
    """
    list_display = ['patient', 'provider_name', 'policy_number', 'copay_amount', 'expiry_date', 'is_active']
    list_filter = ['is_active', 'expiry_date', 'created_at']
    search_fields = ['patient__username', 'provider_name', 'policy_number', 'mental_health_coverage_details']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Insurance Details', {
            'fields': ('patient', 'provider_name', 'policy_number')
        }),
        ('Coverage Information', {
            'fields': ('mental_health_coverage_details', 'copay_amount', 'expiry_date', 'is_active')
        }),
        ('HIPAA Compliance', {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
