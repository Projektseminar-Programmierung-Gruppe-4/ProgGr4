from django.conf.urls import url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from Forum.models import Post
from Forum.models import Comment
from Forum.models import Votes
from Forum.models import Postvotes
from Forum.models import Postreport
from Forum.models import Commentreport
from Forum.models import Department
from .forms import CommentForm, EmployeeForm, PostForm, UserForm, ReportPostForm,ReportCommentForm, DepartmentForm
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

#Funktion für Archivseite mit allen Posts und Kommentaren des Users
def archiv(request):
    posts = Post.objects.filter(author = request.user)
    comments = Comment.objects.filter(author = request.user)
    return render(request, 'Forum/archiv.html', {'posts': posts, 'comments': comments})

def adminpage(request):
    return render (request, 'Forum/adminpage.html')

def reports(request):
    reported_posts = Postreport.objects.all()
    reported_comments = Commentreport.objects.all()
    return render(request, 'Forum/reports.html', {'posts': reported_posts, 'comments': reported_comments})

def permission_overview(request):
    users = User.objects.all().order_by('-is_staff')
    return render(request, 'Forum/permissions.html', {'users': users})

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

def report_post(request, pk):
    entry = Post.objects.get(pk=pk)
    url = '/post/' + str(pk)
    if request.method == "POST":
        form = ReportPostForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.report_date = timezone.now()
            report.post_id = pk
            report.save()
            messages.success(request, "Eintrag erfolgreich gemeldet")
            return redirect(url)
    else:
        form = ReportPostForm()
    form = ReportPostForm()
    return render(request, 'Forum/reportPost.html', {'form': form, 'entry': entry})

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

def report_comment(request, pk):
    entry = Comment.objects.get(pk=pk)
    post = entry.post_id
    url = '/post/' + str(post)
    if request.method == "POST":
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.report_date = timezone.now()
            report.comment_id = pk
            report.save()
            messages.success(request, "Kommentar wurde gemeldet")
            return redirect(url)
    else:
        form = ReportCommentForm()
    return render(request, 'Forum/reportPost.html', {'form': form, 'entry': entry})


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


def release_report(request, pk, type):
    if type == 'comment':
        comment = Commentreport.objects.filter(comment_id = pk)
        comment.delete()
    else:
        post = Postreport.objects.filter(post_id = pk)
        post.delete()
    return redirect('reports')

def delete_report(request,pk,type):
    if type == 'comment':
        comment = Comment.objects.get(pk = pk)
        comment.delete()
    else:
        post = Post.objects.get(pk = pk)
        post.delete()
    return redirect('reports')

def add_department(request):
    departments = Department.objects.all()
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.save()
            return redirect('departments')
    else:
        form = DepartmentForm()
    return render(request, 'Forum/departments.html', {'form': form, 'departments': departments})

def delete_department(request, pk):
    department = Department.objects.get(pk=pk)
    department.delete()
    return redirect('departments')

def set_permission(request, pk):
    user = User.objects.get(pk = pk)
    user.is_staff = True
    user.save()
    return redirect('permissions')

def remove_permission(request, pk):
    user = User.objects.get(pk = pk)   
    user.is_staff = False
    user.save()
    return redirect('permissions')

#Functions for registration, login and Logout of users
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