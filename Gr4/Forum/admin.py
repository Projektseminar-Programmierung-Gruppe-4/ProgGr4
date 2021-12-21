from django.contrib import admin
from .models import Post, Comment, Votes, Postvotes, Employee, Department

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Votes)
admin.site.register(Postvotes)
admin.site.register(Department)
admin.site.register(Employee)
# Register your models here.
