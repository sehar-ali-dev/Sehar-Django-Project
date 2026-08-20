from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from apps.core.decorators import patient_required
from .models import MedicalHistory, MedicalRecord, PatientDocument, InsuranceInformation
from .forms import MedicalHistoryForm, PatientProfileForm, PatientDocumentForm, InsuranceInformationForm
from apps.accounts.models import PatientProfile


@patient_required
def patient_dashboard(request):
    """
    Central patient dashboard showing mental health overview.
    Displays medical history, recent records, documents, and insurance info.
    """
    # Get patient data
    medical_histories = MedicalHistory.objects.filter(
        patient=request.user,
        is_deleted=False
    ).order_by('-diagnosis_date')[:5]
    
    recent_records = MedicalRecord.objects.filter(
        patient=request.user,
        is_deleted=False
    ).order_by('-visit_date')[:5]
    
    recent_documents = PatientDocument.objects.filter(
        patient=request.user,
        is_deleted=False
    ).order_by('-uploaded_at')[:5]
    
    try:
        insurance_info = InsuranceInformation.objects.get(
            patient=request.user,
            is_deleted=False
        )
    except InsuranceInformation.DoesNotExist:
        insurance_info = None
    
    context = {
        'medical_histories': medical_histories,
        'recent_records': recent_records,
        'recent_documents': recent_documents,
        'insurance_info': insurance_info,
    }
    
    return render(request, 'patients/dashboard.html', context)


@patient_required
def medical_history_list(request):
    """
    View all medical history for the patient.
    Shows mental health conditions and treatment history.
    """
    medical_histories = MedicalHistory.objects.filter(
        patient=request.user,
        is_deleted=False
    ).order_by('-diagnosis_date')
    
    context = {
        'medical_histories': medical_histories,
    }
    
    return render(request, 'patients/medical_history.html', context)


@patient_required
def medical_history_add(request):
    """
    Add new medical history entry.
    Allows patients to add mental health conditions.
    """
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = request.user
            medical_history.save()
            messages.success(request, 'Medical history added successfully.')
            return redirect('patients:medical_history_list')
    else:
        form = MedicalHistoryForm()
    
    context = {
        'form': form,
        'action': 'Add Medical History'
    }
    
    return render(request, 'patients/medical_history_form.html', context)


@patient_required
def document_list(request):
    """
    View all patient documents.
    Shows psychological assessments, lab reports, etc.
    """
    documents = PatientDocument.objects.filter(
        patient=request.user,
        is_deleted=False
    ).order_by('-uploaded_at')
    
    context = {
        'documents': documents,
    }
    
    return render(request, 'patients/document_management.html', context)


@patient_required
def document_upload(request):
    """
    Upload new patient document.
    Handles psychological assessments and medical documents.
    """
    if request.method == 'POST':
        form = PatientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('patients:document_list')
    else:
        form = PatientDocumentForm()
    
    context = {
        'form': form,
        'action': 'Upload Document'
    }
    
    return render(request, 'patients/document_form.html', context)


@patient_required
def profile_edit(request):
    """
    Edit patient profile and insurance information.
    Allows updating personal details and insurance coverage.
    """
    # Get or create patient profile
    patient_profile, created = PatientProfile.objects.get_or_create(
        user=request.user
    )
    
    # Get or create insurance information
    insurance_info, created = InsuranceInformation.objects.get_or_create(
        patient=request.user,
        defaults={
            'provider_name': '',
            'policy_number': f'POL-{request.user.username.upper()}001',
            'copay_amount': 0.00,
            'is_active': True
        }
    )
    
    if request.method == 'POST':
        profile_form = PatientProfileForm(
            request.POST,
            instance=patient_profile
        )
        insurance_form = InsuranceInformationForm(
            request.POST,
            instance=insurance_info
        )
        
        if profile_form.is_valid() and insurance_form.is_valid():
            profile_form.save()
            insurance_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('patients:dashboard')
    else:
        profile_form = PatientProfileForm(instance=patient_profile)
        insurance_form = InsuranceInformationForm(instance=insurance_info)
    
    context = {
        'profile_form': profile_form,
        'insurance_form': insurance_form,
    }
    
    return render(request, 'patients/profile_edit.html', context)
