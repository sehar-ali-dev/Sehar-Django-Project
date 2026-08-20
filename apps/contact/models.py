from django.db import models
from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """
    Contact form submissions for MindCare platform.
    HIPAA-aligned: Includes privacy consent and data handling fields.
    """
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('appointment', 'Appointment Request'),
        ('billing', 'Billing Question'),
        ('medical', 'Medical Information'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Contact information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Inquiry details
    inquiry_type = models.CharField(
        max_length=20, 
        choices=INQUIRY_TYPE_CHOICES, 
        default='general'
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    
    # HIPAA Compliance - Privacy and Data Handling
    privacy_consent = models.BooleanField(
        default=False,
        help_text="User consented to privacy policy"
    )
    data_processing_consent = models.BooleanField(
        default=False,
        help_text="User consented to data processing"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="IP address for security tracking"
    )
    user_agent = models.TextField(
        blank=True,
        help_text="Browser user agent for security tracking"
    )
    
    # Response tracking
    responded_at = models.DateTimeField(null=True, blank=True)
    response_notes = models.TextField(blank=True)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['inquiry_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscription(TimeStampedModel):
    """
    Newsletter subscription model for MindCare platform.
    HIPAA-aligned: Includes consent and privacy fields.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    
    # Subscription status
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    # HIPAA Compliance - Privacy and Data Handling
    privacy_consent = models.BooleanField(
        default=False,
        help_text="User consented to privacy policy"
    )
    marketing_consent = models.BooleanField(
        default=False,
        help_text="User consented to marketing communications"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="IP address for security tracking"
    )
    
    # Subscription preferences
    receive_updates = models.BooleanField(default=True)
    receive_promotions = models.BooleanField(default=False)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.email
