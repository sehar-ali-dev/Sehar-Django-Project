from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

# Get the custom User model
User = get_user_model()


class Category(TimeStampedModel):
    """
    Category for organizing blog posts.
    Each post belongs to one category.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete for HIPAA compliance

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    """
    Tags for blog posts.
    Posts can have multiple tags.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete for HIPAA compliance

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel):
    """
    Blog post model with SEO fields for MindCare platform.
    Includes SEO optimization fields for better search engine visibility.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    # Content fields
    excerpt = models.TextField(
        max_length=300, 
        help_text="Short description for listing pages"
    )
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/featured/', 
        null=True, 
        blank=True
    )
    
    # SEO Fields for Search Engine Optimization
    meta_title = models.CharField(
        max_length=60, 
        blank=True, 
        help_text="SEO Title (max 60 chars for Google)"
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="SEO Description (max 160 chars for Google)"
    )
    og_tags = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Open Graph tags for social media sharing"
    )
    canonical_url = models.URLField(
        blank=True, 
        help_text="Canonical URL to prevent duplicate content issues"
    )
    
    # Status and publishing
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    
    # HIPAA Compliance - Soft Delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title
