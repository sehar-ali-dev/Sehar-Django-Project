from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    Abstract model that provides timestamp fields.
    All other models should inherit from this.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hospital(TimeStampedModel):
    """
    Hospital/Clinic model - represents a healthcare facility.
    """
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return self.name


class Department(TimeStampedModel):
    """
    Medical department within a hospital.
    """
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)  # e.g., "Building A, Floor 2"
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['hospital', 'name']
        unique_together = ['hospital', 'name']

    def __str__(self):
        return f"{self.hospital.name} - {self.name}"


class Specialization(TimeStampedModel):
    """
    Medical specialization (e.g., Cardiology, Neurology, Pediatrics).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return self.name