from django.urls import path
from . import views

# URL patterns for the accounts app
# This handles user authentication and profile management

urlpatterns = [
    # Authentication views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile views
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
