from django.contrib.auth import get_user_model

from datetime import date
from typing import Text
from django.core.files.base import equals_lf
from django.test import TestCase
from django.test import Client
from Forum.forms import *


User = get_user_model
class Setup_Class(TestCase):

    def setUp(self):
        
        

        user = get_user_model().objects.create_user('bohnle')
        
        #self.user = User.objects.create(username="TestUser", email="test@gmx.net", password1="maxstinkt123", password2="maxstinkt123", first_name="Manni", last_name="Mammut" )
        self.post = Post.objects.create(author= user, title="Test", text="default text", voteCount= 0 , created_date= '2022-01-04 14:58:25.86806+00')
        #self.employee = Employee.objects.create( birthdate= "1997-02-02", name= "IT")
        #self.department = Department.objects.create(name="IT")
        #self.comment = Comment.objects.create(text="default text")
    

    def valid_data(self):

        form = CommentForm({ 'text': "default text"} ) 
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.text , "default text") 


       


class test_user_form(TestCase):
    

    def test_user_form_valid(self):

        form = UserForm(data= {
            'username':"TestUse", 
            'email':"test@gmx.net", 
            'password1':"maxstinkt123", 
            'password2':"maxstinkt123", 
            'first_name': "Manni", 
            'last_name': "Mammut" })
        self.assertTrue(form.is_valid())
        

    def test_user_form_invalid(self):

        form = UserForm(data= {})
        self.assertFalse(form.is_valid())
        
        

class test_post_form(TestCase):

    
    def test_post_form_valid(self):
        form = PostForm(data={'title': "Test", 'text': "eeww"  })
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.is_valid(), True)
        #self.assertEqual(Post.title , 'Test')
        
    def test_post_form_invald(self):

        form = PostForm(data={ })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

class test_employee_form(TestCase):

    def test_department_form_valid(self):

        form = DepartmentForm(data={'name':"IT"})
        self.assertTrue(form.is_valid())

    def test_department_form_invalid(self):

        form = DepartmentForm(data={'name':""})
        self.assertFalse(form.is_valid())


    def test_employee_form_valid(self):

        form = EmployeeForm(data={'birthdate': '1997-02-02', 'name': "IT"})
        self.assertFalse(form.is_valid())
        #hier noch fixen auf asssertTrue

class test_comment_form(TestCase):

    def test_comment_form_valid(self):

        form = CommentForm(data={'text': "default text"})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):

        form = CommentForm(data={'text': "default text"})
        self.assertTrue(form.is_valid())

class test_reportcomment_form(TestCase):

    def test_reportcomment_form_valid(self):
        form2 = ReportCommentForm(data={'report_message': "shit comment"})
        self.assertTrue(form2.is_valid())




    