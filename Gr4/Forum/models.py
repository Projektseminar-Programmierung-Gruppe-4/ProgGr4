from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.conf import LazySettings, settings
from django.utils import timezone

# Create your models here.

#Klasse Post erstellt neue Tabelle in der Datenbank für die Forumbeiträge
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #categorie = models.ForeignKey()
    title = models.CharField(max_length=200)
    text = models.TextField()
    voteCount = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comments")

    text = models.TextField()
    voteCount = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Votes(models.Model):
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE, related_name="vote")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    like = models.BooleanField()
    dislike = models.BooleanField()

    def __str__(self):
        return self.id

""" class Division():
    name = model. """