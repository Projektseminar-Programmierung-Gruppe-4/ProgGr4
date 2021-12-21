from django.conf.urls import url
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from Forum.models import Comment
from Forum.models import Votes
from Forum.models import Postvotes
from .forms import CommentForm, EmployeeForm, PostForm, UserForm
from django.shortcuts import redirect
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView

# Create your views here.

#eventuelle Filterung hier einbauen
def overview(request):
    posts = Post.objects.all()
    return render(request, 'Forum/base.html', {'posts': posts})

#Views für eine Detailseite, welche einen Post mit seinen dazugehörigen Kommentaren anzeigt 
#und Kommentare hinzufügen lässt
#Eingangsparameter Anfrage und pk des posts
def detail(request, pk):
    #get post mit pk = request pk
    post = get_object_or_404(Post, pk=pk)
    url = "/post/" + pk
    #get alle comments mit fk = post-pk
    comments = post.comments.filter(post_id = pk).order_by('-voteCount')
    #speichern eines Kommentars, wenn Kommentarfeld genutzt wird (request.method = Post)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.voteCount = 0
            comment.post_id = pk
            comment.save()
            return redirect(url)
    #sonst CommentForm() nur anzeigens
    else:
        comment_form = CommentForm()
    return render(request, 'Forum/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.voteCount = 0
            post.save()
            messages.success(request, "Eintrag erfolgreich angelegt")
            return redirect('overview')
    else:
        form = PostForm()
    return render(request, 'Forum/create.html', {'form': form})

def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    url = '/post/' + str(post.id)

    form = CommentForm(request.POST or None, instance=post)
    
    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updatePost.html', {'form': form})

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('overview')

def vote_post(request, pk, vote):
    post = Post.objects.get(pk = pk)
    reaction = vote
    url = '/post/' + pk

    try:
        vote = Postvotes.objects.get(post_id = pk, author_id = request.user)
    except:
        vote = None

    if vote is None:
        Postvotes.objects.create(author_id = request.user.id, post_id = pk, like = False, dislike = False)
    
    vote = Postvotes.objects.get(post_id = pk, author_id = request.user)

    #überprüfen ob like Button, den Request ausgelöst hat
    if reaction == 'like':
        #überprüfen ob Like-Button schon aktiv ist
        if vote.like == True:
            vote.like = False
            post.voteCount -= 1
            vote.save()
            post.save()
            return redirect(url)
        #überprüfen ob dislike button aktiv ist
        elif vote.dislike == True:
            vote.dislike = False
            vote.like = True
            post.voteCount += 2
            vote.save()
            post.save()
            return redirect(url)
        #falls noch kein Button aktiv ist
        else:
            vote.like = True
            post.voteCount += 1
            vote.save()
            post.save()
            return redirect(url)
    
    if reaction == 'dislike':
        if vote.dislike == True:
            vote.dislike = False
            post.voteCount += 1
            vote.save()
            post.save()
            return redirect(url)

        elif vote.like == True:
            vote.like = False
            vote.dislike = True
            post.voteCount -= 2
            vote.save()
            post.save()
            return redirect(url)

        else:
            vote.dislike = True
            post.voteCount -= 1
            vote.save()
            post.save()
            return redirect(url)
    

    return redirect(url)


# Funktionen für Kommentare (update,delete,vote) --> müssen noch geschrieben werden
def update_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post_id
    url = '/post/' + str(post)
    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updateComment.html', {'form': form})

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post_id
    url = '/post/' + str(post)

    comment.delete()
    return redirect(url)


def vote_comment(request, pk, vote):
    comment = Comment.objects.get(pk=pk)
    reaction = vote
    #post um url für return render zu generieren
    post = comment.post_id
    url = '/post/' + str(post)
    try:
        vote = Votes.objects.get(comment_id = pk, author_id = request.user)
    except:
        vote = None

    if vote is None:
        Votes.objects.create(author_id = request.user.id, comment_id = pk, like = False, dislike = False)
    
    vote = Votes.objects.get(comment_id = pk, author_id = request.user)
    
    #überprüfen ob like Button, den Request ausgelöst hat
    if reaction == 'like':
        #überprüfen ob Like-Button schon aktiv ist
        if vote.like == True:
            vote.like = False
            comment.voteCount -= 1
            vote.save()
            comment.save()
            return redirect(url)
        #überprüfen ob dislike button aktiv ist
        elif vote.dislike == True:
            vote.dislike = False
            vote.like = True
            comment.voteCount += 2
            vote.save()
            comment.save()
            return redirect(url)
        #falls noch kein Button aktiv ist
        else:
            vote.like = True
            comment.voteCount += 1
            vote.save()
            comment.save()
            return redirect(url)
    
    if reaction == 'dislike':
        if vote.dislike == True:
            vote.dislike = False
            comment.voteCount += 1
            vote.save()
            comment.save()
            return redirect(url)

        elif vote.like == True:
            vote.like = False
            vote.dislike = True
            comment.voteCount -= 2
            vote.save()
            comment.save()
            return redirect(url)

        else:
            vote.dislike = True
            comment.voteCount -= 1
            vote.save()
            comment.save()
            return redirect(url)


    return redirect(url)

def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        #print(form.is_valid())
        if form.is_valid() and employee_form.is_valid():
            user = form.save()
            
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            login(request, user)
            messages.success(request, "Registrierung erfolgreich")
            return redirect('overview')
        messages.warning(request, "Achtung falsche Eingabe")
    else:
        form = UserForm()
        employee_form = EmployeeForm()
    return render(request, 'Forum/register.html', {'register_form': form, 'employee_form': employee_form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            #print("user: " + str(user))
            if user is not None:
                login(request, user)
                messages.info(request, f"Servus und Willkommen: {username}!")
                print("successfull login")
                return redirect('overview')
            else:
                messages.error(request, "Falscher Username oder Passwort")
        else:
            messages.error(request, "Falscher Username oder Passwort")
    else:
        form = AuthenticationForm()
    return render(request, 'Forum/login.html', {'login_form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "Auf Wiedersehen!")
    return redirect('overview')