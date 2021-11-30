from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post
import re
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "text")


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name" )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    def clean(self):

        #fetching data from from
        super(UserForm, self).clean()

        #extract username, name and last name
        firstname = self.cleaned_data.get('first_name')
        lastname = self.cleaned_data.get('last_name')

        checkFirstname = re.search("[0-9a-zA-Z]*", firstname)
        checkLastname = re.search("[0-9a-zA-Z]*", lastname)

        if checkFirstname != True:
            print('Vornamefehler')
            raise ValidationError("Bitte überprüfe deine Eingabe beim Vornamen")

        if checkLastname != True:
            print('Nachnamenfehler')
            raise ValidationError("Bitte überprüfe deine Eingabe beim Nachnamen")



        return self.cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
