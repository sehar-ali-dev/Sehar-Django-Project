from django import forms
from django.contrib.auth import get_user_model
from .models import MedicalHistory, MedicalRecord, PatientDocument, InsuranceInformation
from apps.accounts.models import PatientProfile

User = get_user_model()


class MedicalHistoryForm(forms.ModelForm):
    """
    Form for adding/updating patient medical history.
    Focuses on mental health conditions and treatment history.
    """
    class Meta:
        model = MedicalHistory
        fields = [
            'condition_name',
            'diagnosis_date',
            'therapy_history',
            'current_medications',
            'notes',
            'status'
        ]
        widgets = {
            'condition_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Major Anxiety Disorder, PTSD, Depression'
            }),
            'diagnosis_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'therapy_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Previous therapy treatments and their outcomes'
            }),
            'current_medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Current psychiatric medications and dosages'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional clinical notes'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'condition_name': 'Mental Health Condition',
            'diagnosis_date': 'Date of Diagnosis',
            'therapy_history': 'Therapy History',
            'current_medications': 'Current Medications',
            'notes': 'Clinical Notes',
            'status': 'Current Status'
        }


class PatientProfileForm(forms.ModelForm):
    """
    Form for updating patient profile information.
    Includes personal details and medical background.
    """
    class Meta:
        model = PatientProfile
        fields = [
            'blood_group',
            'allergies',
            'chronic_conditions',
            'current_medications',
            'insurance_provider',
            'insurance_policy_number'
        ]
        widgets = {
            'blood_group': forms.Select(attrs={
                'class': 'form-select'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Known allergies'
            }),
            'chronic_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Chronic medical conditions'
            }),
            'current_medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Current medications'
            }),
            'insurance_provider': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Insurance provider name'
            }),
            'insurance_policy_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Insurance policy number'
            })
        }
        labels = {
            'blood_group': 'Blood Group',
            'allergies': 'Known Allergies',
            'chronic_conditions': 'Chronic Conditions',
            'current_medications': 'Current Medications',
            'insurance_provider': 'Insurance Provider',
            'insurance_policy_number': 'Policy Number'
        }


class PatientDocumentForm(forms.ModelForm):
    """
    Form for uploading patient documents with file validation.
    Includes file type and size validation for security.
    """
    # Allowed file extensions
    ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'docx']
    # Maximum file size: 5MB in bytes
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    class Meta:
        model = PatientDocument
        fields = [
            'document_title',
            'document_type',
            'file',
            'notes'
        ]
        widgets = {
            'document_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document title or description'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.png,.jpg,.jpeg,.docx'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about the document'
            })
        }
        labels = {
            'document_title': 'Document Title',
            'document_type': 'Document Type',
            'file': 'Upload File',
            'notes': 'Document Notes'
        }
        help_texts = {
            'file': 'Allowed formats: PDF, PNG, JPG, JPEG, DOCX. Maximum size: 5MB'
        }
    
    def clean_file(self):
        """Validate file type and size"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size
            if file.size > self.MAX_FILE_SIZE:
                raise ValidationError(
                    f'File size exceeds 5MB limit. Your file is {file.size / (1024*1024):.2f}MB.'
                )
            
            # Check file extension
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in self.ALLOWED_EXTENSIONS:
                raise ValidationError(
                    f'Invalid file type. Allowed formats: {", ".join(self.ALLOWED_EXTENSIONS).upper()}.'
                )
            
            # Additional check for file content type (MIME type)
            allowed_mime_types = [
                'application/pdf',
                'image/png',
                'image/jpeg',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            
            if hasattr(file, 'content_type'):
                if file.content_type not in allowed_mime_types:
                    raise ValidationError(
                        f'Invalid file content type. Please upload a valid file.'
                    )
        
        return file


class InsuranceInformationForm(forms.ModelForm):
    """
    Form for managing insurance information.
    Focuses on mental health coverage details.
    """
    class Meta:
        model = InsuranceInformation
        fields = [
            'provider_name',
            'policy_number',
            'mental_health_coverage_details',
            'copay_amount',
            'expiry_date',
            'is_active'
        ]
        widgets = {
            'provider_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Insurance provider company name'
            }),
            'policy_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Insurance policy number'
            }),
            'mental_health_coverage_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Details of mental health coverage, sessions covered, etc.'
            }),
            'copay_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Copay amount per session',
                'step': '0.01'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'provider_name': 'Insurance Provider',
            'policy_number': 'Policy Number',
            'mental_health_coverage_details': 'Mental Health Coverage Details',
            'copay_amount': 'Copay Amount',
            'expiry_date': 'Policy Expiry Date',
            'is_active': 'Active Insurance'
        }
