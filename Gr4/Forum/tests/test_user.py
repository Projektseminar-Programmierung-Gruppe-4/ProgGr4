from django import test
import django
from django.contrib import auth
from django.db import reset_queries
from django.http import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, login
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Forum.forms import *


class UserCreationFormTest(TestCase):

    def test_user(self):

        data = {
            'username':"TestUser", 
            'email':"test@gmx.net", 
            'password1':"maxstinkt123", 
            'password2':"maxstinkt123", 
            'first_name': "Manni", 
            'last_name': "Mammut" 
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        
        self.assertTrue(form["username"], "TestsUser")
        #self.assertEqual(form["username"].errors, [force_text(User._meta.get_field('username'))])
        client = Client()
        client.login(username='TestUse', password='maxstinkt123')
        self.assertTrue(client.session) # nicht sicher aber sollte True sein wenn erfolgreiche Session
        
        

        #zugriff home seite
        response_home = client.get("/")
        self.assertEqual(response_home.status_code, 200) 

         #zugriff auf post erstellung
        response_create_post = client.get("/create")
        self.assertEqual(response_create_post.status_code, 200) 

        response_view_post = client.get("/view/1")
        self.assertEqual(response_view_post.status_code, 404) 

        #zugriff home seite
        response_comment = client.get("/comment")
        self.assertEqual(response_comment.status_code, 404) 

        #zugriff home seite
        response_subcomment = client.get("/subcomment")
        self.assertEqual(response_subcomment.status_code, 404) 

        #Zugriff admin page (user kein moderator)
        response_adminpage = client.get("/adminpage")
        self.assertEqual(response_adminpage.status_code, 401)    #keine Berechtigung
        
       
        


User = get_user_model
"""
class UserTestCast(TestCase):
    
    def setUp(self):
        user_a = User(username='cfe', email='max@web.de')
        user_a_pw = 'test123'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)



class BaseTest(TestCase):
    def setUp(self):

        self.register_url = reverse('register_user')
        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page(self):
        self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        

class TestModel(TestCase):

    @classmethod
    def setUp(cls):

        cls.user = User.objects.create_user()
        
        testuser1 = User.objects.create_user("TestUser", "test@gmx.net", "maxstinkt123", "maxstinkt123", "Manni", "Mammut" )
        testuser1.is_admin = True
        testuser1.is_staff = True
        testuser1.save
        
        user = User.objects.create(username='max')
        user.set_password('123qwe')
        user.save()
        client = Client()
        client.login(username='max', password='12qwe')
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_user_exists(self):
        user_count = User.objects.all().count()
        print("Anzahl User: " +str(user_count))
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

"""