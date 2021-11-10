from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class meta:
        model = Post
        fields = {'title', 'text'}
        