from django.urls import path
from . import views

# URL patterns for the contact app
# This handles contact forms and newsletter subscriptions

urlpatterns = [
    # Contact form views
    path('', views.contact_form, name='contact_form'),
    path('success/', views.contact_success, name='contact_success'),
    
    # Newsletter subscription views
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/success/', views.newsletter_success, name='newsletter_success'),
]
