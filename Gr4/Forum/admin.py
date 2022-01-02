from django.contrib import admin
from .models import Commentreport, Post, Comment, Postreport, Votes, Postvotes, Employee, Department

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Votes)
admin.site.register(Postvotes)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Postreport)
admin.site.register(Commentreport)
# Register your models here.
