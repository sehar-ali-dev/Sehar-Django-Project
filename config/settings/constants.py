"""
Project-wide constants for MindCare.
"""

# App constants
APP_NAME = 'MindCare'
APP_VERSION = '1.0.0'

# User roles
USER_ROLES = {
    'admin': 'System Administrator',
    'doctor': 'Doctor',
    'patient': 'Patient',
    'nurse': 'Nurse',
    'receptionist': 'Receptionist',
    'pharmacist': 'Pharmacist',
    'lab_technician': 'Lab Technician',
}

# Pagination
ITEMS_PER_PAGE = 20

# File upload limits
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']

# Appointment durations (in minutes)
APPOINTMENT_DURATIONS = [15, 30, 45, 60]

# Blood groups
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
