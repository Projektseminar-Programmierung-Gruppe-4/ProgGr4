from django.contrib import admin
from .models import Post, Comment, Votes

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Votes)
# Register your models here.
