from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import BlogPost
from .forms import BlogPostForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Home view
def home(request):
    return render(request, "users/home.html")

# User registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

# User login
def login_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "users/login.html", {"form": form})

# User logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

# Blog post views

def post_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': post.get_absolute_url()})
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('post_list')
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': post.get_absolute_url()})
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('post_list')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

@csrf_exempt
@login_required
def ajax_post_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.save()
            return JsonResponse({'status': 'success', 'title': post.title, 'content': post.content})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'invalid request'}, status=400)