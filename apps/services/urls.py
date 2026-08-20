from django.urls import path
from . import views

# URL patterns for the services app
# This handles healthcare services and service categories

urlpatterns = [
    # Service list and detail views
    path('', views.service_list, name='service_list'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Service category views
    path('category/<slug:slug>/', views.category_services, name='category_services'),
]
