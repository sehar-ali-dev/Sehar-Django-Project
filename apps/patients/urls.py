from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient Dashboard
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    
    # Medical History
    path('medical-history/', views.medical_history_list, name='medical_history_list'),
    path('medical-history/add/', views.medical_history_add, name='medical_history_add'),
    
    # Documents
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    
    # Profile
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
