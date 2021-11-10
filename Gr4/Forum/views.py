from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from .forms import PostForm

# Create your views here.

def overview(request):
    posts = Post.objects.all()
    return render(request, 'Forum/index.html', {'posts': posts})

def create_post(request):
    form = PostForm()
    return render(request, 'Forum/create.html', {'form': form})