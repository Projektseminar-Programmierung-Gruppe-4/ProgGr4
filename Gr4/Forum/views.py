from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from .forms import PostForm, UserForm
from django.shortcuts import redirect
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def overview(request):
    posts = Post.objects.all()
    return render(request, 'Forum/base.html', {'posts': posts})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.voteCount = 0
            post.save()
            return redirect('overview')
    else:
        form = PostForm()
    return render(request, 'Forum/create.html', {'form': form})

def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Du bist Registriert du Holzkopf")
            return redirect('overview')
        messages.error(request, "Hah du bist zu dumm zu Scheißen!")

    form = UserForm()
    return render(request, 'Forum/register.html', {'register_form': form})
