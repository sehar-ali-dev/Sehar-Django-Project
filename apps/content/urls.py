from django.urls import path
from . import views

# URL patterns for the content app
# This handles blog posts, categories, and tags

urlpatterns = [
    # Blog post list and detail views
    path('', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Category views
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    
    # Tag views
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
]
