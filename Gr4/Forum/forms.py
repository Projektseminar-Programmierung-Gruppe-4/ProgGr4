from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Comment, Department, Employee, Post, Postreport, Commentreport, Subcomment, Subcommentreport
import re
from django.core.exceptions import ValidationError
from django.conf import settings

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
        #checkFirstname = re.match("[a-zA-Z]", firstname)

        if not re.match("^[a-zA-Z]*$", firstname):
            raise forms.ValidationError("Bitte überprüfe deine Eingabe beim Vornamen")

        return firstname

    def clean_last_name(self):
        #fetching data from from
        #super(UserForm, self).clean()

        lastname = self.cleaned_data.get('last_name')
        #checkLastname = re.match("[a-zA-Z]", lastname)

        if not re.match("^[a-zA-Z]*$", lastname):
            raise forms.ValidationError("Bitte überprüfe deine Eingabe beim Nachnamen")

        return lastname

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Die eingegebenen Passwörter stimmen nicht überein")

        return password2


class EmployeeForm(forms.ModelForm):

    class Meta:
        model= Employee
        fields = ("birthdate", "department")

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)

class SubcommentForm(forms.ModelForm):
    class Meta:
        model = Subcomment
        fields = ("text",)

class ReportPostForm(forms.ModelForm):

    class Meta:
        model = Postreport
        fields = ("report_message",)


class ReportCommentForm(forms.ModelForm):

    class Meta:
        model = Commentreport
        fields = ("report_message",)

class ReportSubcommentForm(forms.ModelForm):

    class Meta:
        model = Subcommentreport
        fields = ("report_message",)
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name",)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        isTaken = Department.objects.filter(name__icontains = name).exists()
        if isTaken == True:
            raise forms.ValidationError("Abteilung ist bereits angelegt")

        return name

