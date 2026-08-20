from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from apps.core.models import TimeStampedModel, Hospital, Department, Specialization


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds healthcare-specific fields and HIPAA compliance.
    """
    ROLE_CHOICES = [
        ('admin', 'System Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('pharmacist', 'Pharmacist'),
        ('lab_technician', 'Lab Technician'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # Basic information
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Emergency contact information
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)

    # Hospital/Department association for staff
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )

    # HIPAA Compliance - Privacy and Data Handling
    privacy_consent_accepted = models.BooleanField(
        default=False,
        help_text="User accepted privacy policy"
    )
    data_processing_consent = models.BooleanField(
        default=False,
        help_text="User consented to data processing"
    )
    terms_accepted = models.BooleanField(
        default=False,
        help_text="User accepted terms of service"
    )
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Security fields for HIPAA compliance
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_users'
    )

    # Fix reverse accessor clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_deleted']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_patient(self):
        return self.role == 'patient'

    @property
    def is_staff_member(self):
        return self.role in ['doctor', 'nurse', 'receptionist', 'pharmacist', 'lab_technician', 'admin']


class DoctorProfile(TimeStampedModel):
    """
    Extended profile for doctors.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        limit_choices_to={'role': 'doctor'}
    )
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.ManyToManyField(Specialization, related_name='doctors')
    qualification = models.TextField()  # e.g., "MBBS, MD (Cardiology)"
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bio = models.TextField(blank=True)
    available_for_telemedicine = models.BooleanField(default=False)
    languages = models.CharField(max_length=200, blank=True)  # Comma-separated
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-rating']
        indexes = [
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class PatientProfile(TimeStampedModel):
    """
    Extended profile for patients.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        limit_choices_to={'role': 'patient'}
    )
    blood_group = models.CharField(max_length=5, blank=True)  # A+, B-, O+, AB+, etc.
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_policy_number = models.CharField(max_length=50, blank=True)
    preferred_hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_patients'
    )
    preferred_doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_patients'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} (Patient)"


class StaffProfile(TimeStampedModel):
    """
    Extended profile for non-doctor staff (nurses, receptionists, etc.).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        limit_choices_to={'role__in': ['nurse', 'receptionist', 'pharmacist', 'lab_technician']}
    )
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField()
    shift = models.CharField(max_length=20, blank=True)  # Morning, Evening, Night
    qualifications = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.get_role_display()})"