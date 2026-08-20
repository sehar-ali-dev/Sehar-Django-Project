from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory


# Service views with actual data


def service_list(request):
    """Display list of all active services"""
    services = Service.objects.filter(status='active', is_deleted=False).select_related('category').order_by('-is_featured', 'name')
    categories = ServiceCategory.objects.filter(is_active=True, is_deleted=False)
    return render(request, 'services/service_list.html', {'services': services, 'categories': categories})


def service_detail(request, slug):
    """Display single service details"""
    service = get_object_or_404(Service, slug=slug, status='active', is_deleted=False)
    return render(request, 'services/service_detail.html', {'service': service})


def category_services(request, slug):
    """Display services in a specific category"""
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True, is_deleted=False)
    services = Service.objects.filter(category=category, status='active', is_deleted=False).select_related('category').order_by('-is_featured', 'name')
    return render(request, 'services/service_list.html', {'services': services, 'category': category})
