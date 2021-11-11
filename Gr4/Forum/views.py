from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from .forms import PostForm, UserForm
from django.shortcuts import redirect
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
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

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            print("user: " + str(user))
            if user is not None:
                login(request, user)
                messages.info(request, f"Servus und Willkommen: {username}!")
                print("successfull login")
                return redirect('overview')
            else:
                messages.error(request, "Falscher Username oder Passwort du Holzkopf")
        else:
            messages.error(request, "Falscher Username oder Passwort du Holzkopf")
    form = AuthenticationForm()
    return render(request, 'Forum/login.html', {'login_form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "Verpiss dich!")
    return redirect('overview')
