from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, NewsletterSubscription
from .forms import ContactMessageForm, NewsletterSubscriptionForm


# Contact views with form processing


def contact_form(request):
    """Display and process contact form using Django Forms with CSRF protection"""
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Create contact message with IP address and user agent
            contact_message = form.save(commit=False)
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact_success')
    else:
        form = ContactMessageForm()
    
    return render(request, 'contact/contact_form.html', {'form': form})


def contact_success(request):
    """Display contact form success page"""
    return render(request, 'contact/contact_success.html')


def newsletter_subscribe(request):
    """Handle newsletter subscription using Django Forms with CSRF protection"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            # Create subscription with IP address
            subscription = form.save(commit=False)
            subscription.ip_address = request.META.get('REMOTE_ADDR')
            subscription.save()
            
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('newsletter_success')
    else:
        form = NewsletterSubscriptionForm()
    
    return render(request, 'contact/newsletter_subscribe.html', {'form': form})


def newsletter_success(request):
    """Display newsletter subscription success page"""
    return render(request, 'contact/newsletter_success.html')
