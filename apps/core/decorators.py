from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def patient_required(view_func):
    """
    Decorator to ensure only patients can access the view.
    Redirects to home with error message if user is not a patient.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'patient':
            messages.error(request, 'Access denied. Patient dashboard only.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def doctor_required(view_func):
    """
    Decorator to ensure only doctors can access the view.
    Redirects to home with error message if user is not a doctor.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'doctor':
            messages.error(request, 'Access denied. Doctor dashboard only.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def staff_required(view_func):
    """
    Decorator to ensure only staff members can access the view.
    Staff members include: doctor, nurse, receptionist, pharmacist, lab_technician, admin.
    Redirects to home with error message if user is not staff.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        staff_roles = ['doctor', 'nurse', 'receptionist', 'pharmacist', 'lab_technician', 'admin']
        if request.user.role not in staff_roles:
            messages.error(request, 'Access denied. Staff dashboard only.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
