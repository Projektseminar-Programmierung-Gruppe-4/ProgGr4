#from django.conf.urls import url
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
from Forum.models import Subcomment
from Forum.models import Subcommentvotes
from Forum.models import Subcommentreport
from .forms import CommentForm, EmployeeForm, PostForm, UserForm, ReportPostForm,ReportCommentForm, DepartmentForm, SubcommentForm,ReportSubcommentForm
from django.shortcuts import redirect
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.db.models import Q
from django.urls import resolve

# Create your views here.

#eventuelle Filterung hier einbauen
def overview(request):
    posts = Post.objects.all()
    filter = request.GET.get('choicefilter')
    search = request.GET.get('search')

    if search != '' and search is not None:
        posts = posts.filter(Q(title__icontains = search) | Q(text__icontains = search))
    if filter != '' and filter is not None:
        if filter == 'votecount':
            posts = posts.order_by('-voteCount')
        else:
            posts = posts.order_by('-created_date')

    return render(request, 'Forum/base.html', {'posts': posts})

#Funktion für Archivseite mit allen Posts und Kommentaren des Users
def archiv(request):
    posts = Post.objects.filter(author = request.user)
    comments = Comment.objects.filter(author = request.user)
    subcomments = Subcomment.objects.filter(author = request.user)
    return render(request, 'Forum/archiv.html', {'posts': posts, 'comments': comments,'subcomments': subcomments})

#Funktion zum anzeigen der Adminseite
def adminpage(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
    return render (request, 'Forum/adminpage.html')

#Funktion zum anzeigen der gemeldeten Posts,Kommentare und Antworten
def reports(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
        
    reported_posts = Postreport.objects.all()
    reported_comments = Commentreport.objects.all()
    reported_subcomments = Subcommentreport.objects.all()
    return render(request, 'Forum/reports.html', {'posts': reported_posts, 'comments': reported_comments, 'subcomments': reported_subcomments})

def permission_overview(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
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

def vote(request, pk, vote, typ):
    reaction = vote
    url = request.META.get('HTTP_REFERER')
    if typ == 'post':
        entry = Post.objects.get(pk = pk)

        try:
            vote = Postvotes.objects.get(post_id = pk, author_id = request.user)
        except:
            vote = None

        if vote is None:
            Postvotes.objects.create(author_id = request.user.id, post_id = pk, like = False, dislike = False)
        
        vote = Postvotes.objects.get(post_id = pk, author_id = request.user)
    elif typ == 'comment':
        entry = Comment.objects.get(pk=pk)
        try:
            vote = Votes.objects.get(comment_id = pk, author_id = request.user)
        except:
            vote = None

        if vote is None:
            Votes.objects.create(author_id = request.user.id, comment_id = pk, like = False, dislike = False)
        
        vote = Votes.objects.get(comment_id = pk, author_id = request.user)
    else:
        entry = Subcomment.objects.get(pk=pk)
        try:
            vote = Subcommentvotes.objects.get(subcomment_id = pk, author_id = request.user)
        except:
            vote = None

        if vote is None:
            Subcommentvotes.objects.create(author_id = request.user.id, subcomment_id = pk, like = False, dislike = False)
        
        vote = Subcommentvotes.objects.get(subcomment_id = pk, author_id = request.user)


    #überprüfen ob like Button, den Request ausgelöst hat
    if reaction == 'like':
        #überprüfen ob Like-Button schon aktiv ist
        if vote.like == True:
            vote.like = False
            entry.voteCount -= 1
            vote.save()
            entry.save()
            return redirect(url)
        #überprüfen ob dislike button aktiv ist
        elif vote.dislike == True:
            vote.dislike = False
            vote.like = True
            entry.voteCount += 2
            vote.save()
            entry.save()
            return redirect(url)
        #falls noch kein Button aktiv ist
        else:
            vote.like = True
            entry.voteCount += 1
            vote.save()
            entry.save()
            return redirect(url)
    
    if reaction == 'dislike':
        if vote.dislike == True:
            vote.dislike = False
            entry.voteCount += 1
            vote.save()
            entry.save()
            return redirect(url)

        elif vote.like == True:
            vote.like = False
            vote.dislike = True
            entry.voteCount -= 2
            vote.save()
            entry.save()
            return redirect(url)

        else:
            vote.dislike = True
            entry.voteCount -= 1
            vote.save()
            entry.save()
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

#Funktionen für subcomments
def detail_comment(request, pk):
    #get alle comments mit fk = post-pk
    comment = Comment.objects.get(pk=pk)
    post = Post.objects.get(pk=comment.post_id)
    subcomments = Subcomment.objects.filter(comment_id = pk).order_by('-voteCount')
    url = "/comment/" + str(comment.id) + "/detail/"
    #speichern eines Kommentars, wenn Kommentarfeld genutzt wird (request.method = Post)
    if request.method == "POST":
        subcomment_form = SubcommentForm(request.POST)
        if subcomment_form.is_valid():
            subcomment = subcomment_form.save(commit=False)
            subcomment.author = request.user
            subcomment.voteCount = 0
            subcomment.comment_id = pk
            subcomment.save()
            return redirect(url)
    #sonst CommentForm() nur anzeigens
    else:
        subcomment_form = SubcommentForm()
    return render(request, 'Forum/commentDetail.html', {'post': post, 'comment': comment,'subcomments': subcomments, 'form': subcomment_form})

def update_subcomment(request, pk):
    subcomment = Subcomment.objects.get(pk=pk)
    comment = subcomment.comment_id
    url = '/comment/' + str(comment) + '/detail/'
    form = SubcommentForm(request.POST or None, instance=subcomment)

    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updateComment.html', {'form': form})

def delete_subcomment(request, pk):
    subcomment = Subcomment.objects.get(pk=pk)
    comment = subcomment.comment_id
    url = '/comment/' + str(comment) + '/detail/'

    subcomment.delete()
    return redirect(url)

def report_subcomment(request, pk):
    entry = Subcomment.objects.get(pk=pk)
    comment = entry.comment_id
    url = '/comment/' + str(comment) + '/detail/'
    if request.method == "POST":
        form = ReportSubcommentForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.report_date = timezone.now()
            report.subcomment_id = pk
            report.save()
            messages.success(request, "Kommentar wurde gemeldet")
            return redirect(url)
    else:
        form = ReportSubcommentForm()
    return render(request, 'Forum/reportPost.html', {'form': form, 'entry': entry})


def release_report(request, pk, type):
    if type == 'comment':
        comment = Commentreport.objects.filter(comment_id = pk)
        comment.delete()
    elif type =='post':
        post = Postreport.objects.filter(post_id = pk)
        post.delete()
    else:
        subcomment = Subcommentreport.objects.filter(subcomment_id=pk)
        subcomment.delete()
    return redirect('reports')

def delete_report(request,pk,type):
    if type == 'comment':
        comment = Comment.objects.get(pk = pk)
        comment.delete()
    elif type == 'post':
        post = Post.objects.get(pk = pk)
        post.delete()
    else:
        subcomment = Subcomment.objects.get(pk=pk)
        subcomment.delete()
    return redirect('reports')

def add_department(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
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