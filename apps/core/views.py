from django.shortcuts import render


# Home page view
def home(request):
    """Display the home page"""
    return render(request, 'home.html')
