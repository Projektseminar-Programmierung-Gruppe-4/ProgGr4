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
from Forum.models import Employee
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

# Here are the functions, which fills the templates with life
# Our views is function based structured


##############################function for view sites, eg. overview, detail, commentdetail etc##############
#function for base.html, records are sorted depending on filter parameters 
def overview(request):
    posts = Post.objects.all()
    filter = request.GET.get('choicefilter')
    search = request.GET.get('search')

    #check if search term is in filter 
    if search != '' and search is not None:
        posts = posts.filter(Q(title__icontains = search) | Q(text__icontains = search))

    #check if a choice in the filter is applied
    if filter != '' and filter is not None:
        if filter == 'votecount-desc':
            posts = posts.order_by('-voteCount')
        elif filter == 'votecount-asc':
            posts = posts.order_by('voteCount')
        elif filter == 'date-old':
            posts = posts.order_by('created_date')
        else:
            posts = posts.order_by('-created_date')

    return render(request, 'Forum/base.html', {'posts': posts})

#Function for archive page with all posts,comments and subcomments of the user
def archiv(request):
    posts = Post.objects.filter(author = request.user)
    comments = Comment.objects.filter(author = request.user)
    subcomments = Subcomment.objects.filter(author = request.user)
    return render(request, 'Forum/archiv.html', {'posts': posts, 'comments': comments,'subcomments': subcomments})

#function to show adminsite, only available with is_staff status 
def adminpage(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
    return render (request, 'Forum/adminpage.html')

#function to show all reported posts, comments and subcomments, only available with is_staff
def reports(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
        
    reported_posts = Postreport.objects.all()
    reported_comments = Commentreport.objects.all()
    reported_subcomments = Subcommentreport.objects.all()
    return render(request, 'Forum/reports.html', {'posts': reported_posts, 'comments': reported_comments, 'subcomments': reported_subcomments})

#function for permission overview site
def permission_overview(request):
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
    users = User.objects.all().order_by('-is_staff')
    return render(request, 'Forum/permissions.html', {'users': users})

#Views for a detail page, which displays a post with its associated comments. 
#and lets you add comments
#input parameters request and pk of the post
def detail(request, pk):
    #get post with pk = request pk
    post = get_object_or_404(Post, pk=pk)
    url = "/post/" + pk
    #get all comments with fk = post-pk
    comments = post.comments.filter(post_id = pk).order_by('-voteCount')
    
    #save a comment, if commentfield is used(request.method = Post)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.voteCount = 0
            comment.post_id = pk
            comment.save()
            return redirect(url)
    #wenn method is not post, show emtpy Form
    else:
        comment_form = CommentForm()
    return render(request, 'Forum/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

#function for comment detail page, input param pk
#page shows: post + comment + subcomment for this comment
def detail_comment(request, pk):
    #get comments, posts and subcomments with comment_pk
    comment = Comment.objects.get(pk=pk)
    post = Post.objects.get(pk=comment.post_id)
    subcomments = Subcomment.objects.filter(comment_id = pk).order_by('-voteCount')
    url = "/comment/" + str(comment.id) + "/detail/"
    #save the subcomment if form is used
    if request.method == "POST":
        subcomment_form = SubcommentForm(request.POST)
        if subcomment_form.is_valid():
            subcomment = subcomment_form.save(commit=False)
            subcomment.author = request.user
            subcomment.voteCount = 0
            subcomment.comment_id = pk
            subcomment.save()
            return redirect(url)
    #else only show empty Form
    else:
        subcomment_form = SubcommentForm()
    return render(request, 'Forum/commentDetail.html', {'post': post, 'comment': comment,'subcomments': subcomments, 'form': subcomment_form})


#########################functions to create, update, delete and report posts##########################
#create post over PostForm
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

#function for reporting a post, user can report a post with a report commment
def report_post(request, pk):
    #get post over pk
    entry = Post.objects.get(pk=pk)
    url = '/post/' + str(pk)
    if request.method == "POST":
        form = ReportPostForm(request.POST)
        if form.is_valid():
            #save post with comment to Postreport Modell
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

#function for updating post: title+text
def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    url = '/post/' + str(post.id)

    form = CommentForm(request.POST or None, instance=post)
    
    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updatePost.html', {'form': form})

#delete post via pk
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('overview')


#voting function to vote post, comment or subcomment
#entry parameters are pk of the entry, vote(like or dislike) and type of entry(post,comment or subcomment)
def vote(request, pk, vote, typ):
    reaction = vote
    #get url from page from which the request came
    url = request.META.get('HTTP_REFERER')

    #if-else with parameter typ to get the right models to update or create
    #(post-postvotes, comment-commentvotes or subcomment-subcommentvotes)
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


    #check if request is from like button
    if reaction == 'like':
        #check if like-button is already active
        if vote.like == True:
            vote.like = False
            entry.voteCount -= 1
            vote.save()
            entry.save()
            return redirect(url)
        #check if dislike-button is already active
        elif vote.dislike == True:
            vote.dislike = False
            vote.like = True
            entry.voteCount += 2
            vote.save()
            entry.save()
            return redirect(url)
        #if no button is active
        else:
            vote.like = True
            entry.voteCount += 1
            vote.save()
            entry.save()
            return redirect(url)
    #check if request is from like button
    if reaction == 'dislike':
        #check if dislike-button is already active
        if vote.dislike == True:
            vote.dislike = False
            entry.voteCount += 1
            vote.save()
            entry.save()
            return redirect(url)

        #check if like-button is already active
        elif vote.like == True:
            vote.like = False
            vote.dislike = True
            entry.voteCount -= 2
            vote.save()
            entry.save()
            return redirect(url)

        #if no button is active
        else:
            vote.dislike = True
            entry.voteCount -= 1
            vote.save()
            entry.save()
            return redirect(url)
    

    return redirect(url)


#################### functions for comments (update,delete,report, detail page)#########################

#update comment text
def update_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post_id
    url = '/post/' + str(post)
    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updateComment.html', {'form': form})

#delete comment
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post_id
    url = '/post/' + str(post)

    comment.delete()
    return redirect(url)

#report comment via pk
def report_comment(request, pk):
    #get comment via pk
    entry = Comment.objects.get(pk=pk)
    post = entry.post_id
    url = '/post/' + str(post)
    if request.method == "POST":
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            #save comment with report comment into ReportComment Model
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

#################################functions for subcomments##################################

#update subcomments via pk and SubcommentForm
def update_subcomment(request, pk):
    subcomment = Subcomment.objects.get(pk=pk)
    comment = subcomment.comment_id
    url = '/comment/' + str(comment) + '/detail/'
    form = SubcommentForm(request.POST or None, instance=subcomment)

    if form.is_valid():
        form.save()
        return redirect(url)
    
    return render(request, 'Forum/updateComment.html', {'form': form})

#delete subcomment via pk
def delete_subcomment(request, pk):
    subcomment = Subcomment.objects.get(pk=pk)
    comment = subcomment.comment_id
    url = '/comment/' + str(comment) + '/detail/'

    subcomment.delete()
    return redirect(url)

#report subcomment via pk
def report_subcomment(request, pk):
    #get the subcomment via pk=pk
    entry = Subcomment.objects.get(pk=pk)
    comment = entry.comment_id
    url = '/comment/' + str(comment) + '/detail/'
    if request.method == "POST":
        form = ReportSubcommentForm(request.POST)
        if form.is_valid():
            #save the subcomment and its report comment into ReportSubcommentForm
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

###############################functions for adminpage#########################

#release the report, input param pk an type(post, comment, subcomment)
def release_report(request, pk, type):
    #get the right object depending to typ and pk
    #delete it only from the report table
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

#delete the report (post,comment or subcomment)
def delete_report(request,pk,type):
    #get the right object depending to typ and pk
    #delete it (linked Object in report table will automatically be deleted because of on_delete)
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

#function for showing departments + adding 
def add_department(request):
    #only available with is_staff rights
    if request.user.is_staff == False:
        return HttpResponse('Unauthorized', status=401)
    departments = Department.objects.all()
    #adding new department via Post-Request and Departmentform
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.save()
            return redirect('departments')
    else:
        form = DepartmentForm()
    return render(request, 'Forum/departments.html', {'form': form, 'departments': departments})

#delete the department via pk
def delete_department(request, pk):
    department = Department.objects.get(pk=pk)
    department.delete()
    return redirect('departments')

#set is_staff for user with pk = true
def set_permission(request, pk):
    user = User.objects.get(pk = pk)
    user.is_staff = True
    user.save()
    return redirect('permissions')

#set is_staff for user with pk = true
def remove_permission(request, pk):
    user = User.objects.get(pk = pk)   
    user.is_staff = False
    user.save()
    return redirect('permissions')

#####################################Functions for registration,update, login and Logout of users#####################

#register user via User Form  and EmployeeForm (fk=user.pk )
def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)

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

#update the user
def update_user(request,pk):
    user = User.objects.get(pk=pk)

    #check if employee with fk = user.pk exists
    try:
        employee = Employee.objects.get(user_id=pk)
    except:
        employee = None
    
    #if employee exists -> use data from user + employee to update
    if employee != None:
        form = UserForm(request.POST or None, instance=user)
        employee_form = EmployeeForm(request.POST or None, instance=employee)

        if form.is_valid() and employee_form.is_valid():
            user = form.save()
            employee_form.save()
            login(request, user)
            messages.success(request, "Profil erfolgreich bearbeitet")
            return redirect('overview')

    #if employee doesnt exists -> use data from user and empty employee form to update
    else:
        form = UserForm(request.POST or None, instance=user)
        employee_form = EmployeeForm(request.POST)

        if form.is_valid() and employee_form.is_valid():
            user = form.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            login(request, user)
            messages.success(request, "Profil erfolgreich bearbeitet")
            return redirect('overview')

    
    return render(request, 'Forum/updateUser.html', {'form': form, 'employee_form': employee_form})

#login via AuthenticationForm
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            
            if user is not None:
                login(request, user)
                messages.info(request, f"Servus und Willkommen: {username}!")
                return redirect('overview')
            else:
                messages.error(request, "Falscher Username oder Passwort")
        else:
            messages.error(request, "Falscher Username oder Passwort")
    else:
        form = AuthenticationForm()
    return render(request, 'Forum/login.html', {'login_form': form})

#logout user via django-logout function
def logout_user(request):
    logout(request)
    messages.info(request, "Auf Wiedersehen!")
    return redirect('overview')