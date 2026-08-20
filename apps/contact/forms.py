from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage, NewsletterSubscription


class ContactMessageForm(forms.ModelForm):
    """
    Django ModelForm for contact messages with CSRF protection and automatic validation.
    Replaces manual POST processing with proper Django form handling.
    """
    class Meta:
        model = ContactMessage
        fields = [
            'name',
            'email',
            'phone',
            'inquiry_type',
            'subject',
            'message',
            'privacy_consent',
            'data_processing_consent'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (optional)'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your inquiry',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message',
                'required': True
            }),
            'privacy_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'required': True
            }),
            'data_processing_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'required': True
            })
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'inquiry_type': 'Inquiry Type',
            'subject': 'Subject',
            'message': 'Message',
            'privacy_consent': 'I accept the privacy policy',
            'data_processing_consent': 'I consent to data processing'
        }
        help_texts = {
            'privacy_consent': 'Required for processing your inquiry',
            'data_processing_consent': 'Required for processing your inquiry'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make consent fields required
        self.fields['privacy_consent'].required = True
        self.fields['data_processing_consent'].required = True
    
    def clean_email(self):
        """Validate email format"""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
        return email
    
    def clean_message(self):
        """Sanitize message content"""
        message = self.cleaned_data.get('message')
        if message:
            # Basic sanitization - strip excessive whitespace
            message = ' '.join(message.split())
            # Prevent extremely long messages
            if len(message) > 5000:
                raise forms.ValidationError('Message is too long. Maximum 5000 characters allowed.')
        return message


class NewsletterSubscriptionForm(forms.ModelForm):
    """
    Django ModelForm for newsletter subscriptions with CSRF protection.
    Replaces manual POST processing with proper Django form handling.
    """
    class Meta:
        model = NewsletterSubscription
        fields = [
            'email',
            'name',
            'privacy_consent',
            'marketing_consent'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            }),
            'privacy_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'required': True
            }),
            'marketing_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'email': 'Email Address',
            'name': 'Name',
            'privacy_consent': 'I accept the privacy policy',
            'marketing_consent': 'I want to receive marketing emails'
        }
        help_texts = {
            'privacy_consent': 'Required for newsletter subscription'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make privacy consent required
        self.fields['privacy_consent'].required = True
    
    def clean_email(self):
        """Validate email format and check for existing subscription"""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
            
            # Check if already subscribed
            if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
                raise forms.ValidationError('This email is already subscribed to our newsletter.')
        
        return email
