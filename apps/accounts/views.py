from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def login_view(request):
    """Handle user login with account lockout protection"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if account is locked
            if user.account_locked:
                # Check if lockout period has expired (30 minutes)
                if user.locked_at and (timezone.now() - user.locked_at).total_seconds() < 1800:
                    messages.error(
                        request, 
                        'Your account has been locked due to multiple failed login attempts. '
                        'Please try again later or contact support.'
                    )
                    return render(request, 'accounts/login.html', {'form': form})
                else:
                    # Unlock account after 30 minutes
                    user.account_locked = False
                    user.failed_login_attempts = 0
                    user.locked_at = None
                    user.save()
            
            # Successful login - reset failed attempts
            user.failed_login_attempts = 0
            user.last_login_ip = request.META.get('REMOTE_ADDR')
            user.save()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            # Failed login - increment failed attempts
            username = request.POST.get('username')
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(username=username)
                
                user.failed_login_attempts += 1
                
                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.account_locked = True
                    user.locked_at = timezone.now()
                    messages.error(
                        request,
                        'Your account has been locked due to multiple failed login attempts. '
                        'Please try again in 30 minutes or contact support.'
                    )
                else:
                    remaining_attempts = 5 - user.failed_login_attempts
                    messages.error(
                        request,
                        f'Invalid credentials. {remaining_attempts} attempt(s) remaining before account lockout.'
                    )
                
                user.save()
            except User.DoesNotExist:
                # User doesn't exist - don't reveal this
                messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set privacy consent and data processing consent by default for new users
            user.privacy_consent_accepted = True
            user.data_processing_consent = True
            user.terms_accepted = True
            user.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """Display user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """Handle profile editing"""
    return render(request, 'accounts/profile_edit.html', {'user': request.user})
