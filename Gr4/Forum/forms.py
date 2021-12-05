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

    def clean_first_name(self):

        #fetching data from from
        #super(UserForm, self).clean()

        #extract username, name and last name
        firstname = self.cleaned_data.get('first_name')

        checkFirstname = re.search("[a-zA-Z]*", firstname)

        if checkFirstname != True:
            print('Vornamefehler')
            raise forms.ValidationError("Bitte überprüfe deine Eingabe beim Vornamen")

        return self.cleaned_data

    def clean_last_name(self):
        #fetching data from from
        #super(UserForm, self).clean()

        lastname = self.cleaned_data.get('last_name')

        checkLastname = re.search("[a-zA-Z]*", lastname)

        if checkLastname != True:
            print('Nachnamenfehler')
            raise ValidationError("Bitte überprüfe deine Eingabe beim Nachnamen")

        return self.cleaned_data
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Die eingegebenen Passwörter stimmen nicht überein")
            
        return super().clean_password2()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
