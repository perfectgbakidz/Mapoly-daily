from django.http import JsonResponse
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BlogPostForm, CommentForm,CustomUserCreationForm
from .models import Profile, Comment,BlogPost,Category,Profile
from django.contrib.auth.models import User
from django import forms

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            # ✅ Ensure Profile is created only if it doesn't exist
            Profile.objects.get_or_create(user=user)

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})

# User Profile View
@login_required
def profile(request):
    return render(request, 'blog/profile.html')

# List All Blog Posts (Home Page)
def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})

# Blog Post Detail Page
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    form = CommentForm()
    return render(request, 'blog/blog_detail.html', {'post': post})

# Create New Blog Post
@login_required
def blog_create(request):
    categories = Category.objects.all()  # Fetch all categories
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your blog post has been created successfully!")
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'categories': categories})

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure Profile exists

    if request.method == "POST":
        bio = request.POST.get("bio", "").strip() 
        if bio:
            profile.bio = bio
        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]
        profile.save()  
        messages.success(request, "Profile updated successfully!")

    return redirect("profile")  

# Update Blog Post
@login_required
def blog_update(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your blog post has been updated!")
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form, 'categories': categories})


# Delete Blog Post
@login_required
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Your blog post has been deleted.")
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})

@login_required
def blog_like(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

# Add a Comment
@login_required
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('blog_detail', slug=post.slug)  # ✅ Redirect back to the post
    return redirect('blog_detail', slug=post.slug)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(published=True).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})


@login_required
def user_dashboard(request):
    user_posts = BlogPost.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(user=request.user)
    return render(request, 'blog/dashboard.html', {'posts': user_posts, 'comments': user_comments})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def search(request):
    query = request.GET.get('q', '')
    results = BlogPost.objects.filter(title__icontains=query, published=True) if query else []
    return render(request, 'blog/search_results.html', {'query': query, 'results': results})

