from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.utils import timezone

# Create your views here.

def overview(request):
    posts = Post.objects.all()
    return render(request, 'Forum/index.html', {'posts': posts})

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

