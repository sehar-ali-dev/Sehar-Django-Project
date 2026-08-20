from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.accounts.models import User, PatientProfile


class MedicalHistory(TimeStampedModel):
    """
    Medical history model for tracking patient mental health conditions.
    Stores psychiatric diagnoses, therapy history, and treatment progress.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_treatment', 'In Treatment'),
        ('in_remission', 'In Remission'),
        ('resolved', 'Resolved'),
        ('chronic', 'Chronic'),
    ]
    
    # Patient relationship
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_histories',
        limit_choices_to={'role': 'patient'}
    )
    
    # Mental health condition details
    condition_name = models.CharField(
        max_length=200,
        help_text="e.g., Major Anxiety Disorder, PTSD, Depression, Bipolar Disorder"
    )
    diagnosis_date = models.DateField(
        help_text="Date when condition was diagnosed"
    )
    therapy_history = models.TextField(
        blank=True,
        help_text="Previous therapy treatments and their outcomes"
    )
    current_medications = models.TextField(
        blank=True,
        help_text="Current psychiatric medications and dosages"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional clinical notes"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current status of the condition"
    )
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-diagnosis_date', 'condition_name']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.condition_name}"


class MedicalRecord(TimeStampedModel):
    """
    Individual medical/psychiatric visit records.
    Tracks therapy sessions, consultations, and treatment plans.
    """
    # Patient relationship
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_records',
        limit_choices_to={'role': 'patient'}
    )
    
    # Visit details
    doctor_name = models.CharField(
        max_length=200,
        help_text="Name of the doctor or therapist"
    )
    visit_date = models.DateTimeField(
        help_text="Date and time of the visit"
    )
    mental_health_diagnosis = models.TextField(
        blank=True,
        help_text="Primary mental health diagnosis or assessment"
    )
    therapy_notes = models.TextField(
        blank=True,
        help_text="Detailed therapy session notes and observations"
    )
    prescription_details = models.TextField(
        blank=True,
        help_text="Medications prescribed with dosages"
    )
    recommended_treatment_plan = models.TextField(
        blank=True,
        help_text="Recommended treatment plan and next steps"
    )
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', 'visit_date']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.visit_date.strftime('%Y-%m-%d')}"


class PatientDocument(TimeStampedModel):
    """
    Patient documents for psychological assessments, lab reports, etc.
    Secure document storage for mental health records.
    """
    DOCUMENT_TYPE_CHOICES = [
        ('psychological_assessment', 'Psychological Assessment'),
        ('lab_report', 'Lab Report'),
        ('psychiatric_evaluation', 'Psychiatric Evaluation'),
        ('self_report_scale', 'Self-Report Scale'),
        ('therapy_notes', 'Therapy Notes'),
        ('insurance_document', 'Insurance Document'),
        ('other', 'Other'),
    ]
    
    # Patient relationship
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_documents',
        limit_choices_to={'role': 'patient'}
    )
    
    # Document details
    document_title = models.CharField(
        max_length=200,
        help_text="Title or description of the document"
    )
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        help_text="Type of document"
    )
    file = models.FileField(
        upload_to='patient_documents/%Y/%m/',
        help_text="Upload the document file"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when document was uploaded"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the document"
    )
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['patient', 'document_type']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.document_title}"


class InsuranceInformation(TimeStampedModel):
    """
    Insurance information for mental health coverage.
    Tracks insurance providers, coverage details, and copay information.
    """
    # Patient relationship
    patient = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='insurance_info',
        limit_choices_to={'role': 'patient'}
    )
    
    # Insurance details
    provider_name = models.CharField(
        max_length=200,
        help_text="Insurance provider company name"
    )
    policy_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Insurance policy number"
    )
    mental_health_coverage_details = models.TextField(
        blank=True,
        help_text="Details of mental health coverage, sessions covered, etc."
    )
    copay_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Copay amount per session"
    )
    expiry_date = models.DateField(
        help_text="Insurance policy expiry date"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the insurance is currently active"
    )
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_active', 'expiry_date']
        indexes = [
            models.Index(fields=['patient', 'is_active']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.patient.username} - {self.provider_name}"
