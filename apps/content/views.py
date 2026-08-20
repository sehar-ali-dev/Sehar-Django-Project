from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import BlogPost, Category, Tag


# Blog views with actual data


def blog_list(request):
    """Display list of all published blog posts"""
    posts = BlogPost.objects.filter(status='published', is_deleted=False).select_related('category').order_by('-published_at')
    categories = Category.objects.filter(is_active=True, is_deleted=False)
    return render(request, 'content/blog_list.html', {'posts': posts, 'categories': categories})


def blog_detail(request, slug):
    """Display single blog post"""
    post = get_object_or_404(BlogPost, slug=slug, status='published', is_deleted=False)
    # Increment view count using F() expression for atomic update
    BlogPost.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
    return render(request, 'content/blog_detail.html', {'post': post})


def category_posts(request, slug):
    """Display posts in a specific category"""
    category = get_object_or_404(Category, slug=slug, is_active=True, is_deleted=False)
    posts = BlogPost.objects.filter(category=category, status='published', is_deleted=False).select_related('category').order_by('-published_at')
    return render(request, 'content/blog_list.html', {'posts': posts, 'category': category})


def tag_posts(request, slug):
    """Display posts with a specific tag"""
    tag = get_object_or_404(Tag, slug=slug, is_deleted=False)
    posts = BlogPost.objects.filter(tags=tag, status='published', is_deleted=False).select_related('category').prefetch_related('tags').order_by('-published_at')
    return render(request, 'content/blog_list.html', {'posts': posts, 'tag': tag})
