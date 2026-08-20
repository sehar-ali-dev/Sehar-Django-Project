from django.db import models
from apps.core.models import TimeStampedModel


class ServiceCategory(TimeStampedModel):
    """
    Category for organizing healthcare services.
    Examples: Mental Health, Rehabilitation, Therapy, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name for UI")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete for HIPAA compliance

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(TimeStampedModel):
    """
    Healthcare service model for MindCare platform.
    Represents services offered by the healthcare facility.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('coming_soon', 'Coming Soon'),
    ]
    
    # Basic fields
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='services'
    )
    
    # Service details
    short_description = models.CharField(
        max_length=200, 
        help_text="Brief description for listing pages"
    )
    detailed_description = models.TextField(help_text="Full service description")
    
    # Pricing and duration
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Service price in local currency"
    )
    duration_minutes = models.PositiveIntegerField(
        help_text="Service duration in minutes"
    )
    
    # Service availability
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    is_featured = models.BooleanField(default=False)
    
    # Image and media
    service_image = models.ImageField(
        upload_to='services/images/', 
        null=True, 
        blank=True
    )
    
    # SEO Fields for Search Engine Optimization
    meta_title = models.CharField(
        max_length=60, 
        blank=True, 
        help_text="SEO Title (max 60 chars)"
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="SEO Description (max 160 chars)"
    )
    
    # Additional information
    requirements = models.TextField(
        blank=True, 
        help_text="Special requirements or prerequisites"
    )
    what_to_expect = models.TextField(
        blank=True, 
        help_text="What patients should expect during the service"
    )
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_featured', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name
