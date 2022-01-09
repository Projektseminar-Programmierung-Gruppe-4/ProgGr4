from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import models
from django.conf import LazySettings, settings
from django.db.models.fields import NullBooleanField
from django.utils import timezone

#from Forum.tests.tests import User

# Create your models here.

#class for posts in the Forum with fk = user_id
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    #categorie = models.ForeignKey()
    title = models.CharField(max_length=200)
    text = models.TextField()
    voteCount = models.IntegerField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#class for comments with fk = post_id,user_id
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comments", blank=True, null=True)

    text = models.TextField()
    voteCount = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#class for subcomments with fk = comment_id,user_id
class Subcomment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, related_name="subcomments", blank=True, null=True)

    text = models.TextField()
    voteCount = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#class for storing the status of the votes for Comments depending on the user
class Votes(models.Model):
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE, related_name="vote", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    like = models.BooleanField()
    dislike = models.BooleanField()

    def __str__(self):
        return self.id

#class for storing the status of the votes for Posts depending on the user
class Postvotes(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name="postvote", blank=True , null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , blank=True, null=True)

    like = models.BooleanField()
    dislike = models.BooleanField()

    def __str__(self):
        return self.id

#class for storing the status of the votes for subcomments depending on the user
class Subcommentvotes(models.Model):
    subcomment = models.ForeignKey(Subcomment,on_delete = models.CASCADE, related_name="subcommentvote" , blank=True , null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , blank=True, null=True)

    like = models.BooleanField()
    dislike = models.BooleanField()

    def __str__(self):
        return self.id


#class for the departments, user can be assigned to
class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Class for the fields which are not to be found in the user model (birthdate and department)
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birthdate = models.DateField()
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, related_name="department", null=True)

    def __str__(self):
        return self.user.username

#class to store reported posts(fk=user_id,post_id)
class Postreport(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name="post")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateTimeField(blank=True, null=True)
    report_message = models.TextField()

    def __str__(self):
        return self.post.title

#class to store reported comments (fk=user_id,comment_id)
class Commentreport(models.Model):
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE, related_name="comment")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateTimeField(blank=True, null=True)
    report_message = models.TextField()

    def __str__(self):
        return self.comment.text

#class to store reported comments (fk=user_id,subcomment_id)
class Subcommentreport(models.Model):
    subcomment = models.ForeignKey(Subcomment,on_delete = models.CASCADE, related_name="subcomment")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateTimeField(blank=True, null=True)
    report_message = models.TextField()

    def __str__(self):
        return self.subcomment.text
        