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


class UserCreationFormTest(TestCase):

    def test_user(self):

        data = {
            'username':"TestUse", 
            'email':"test@gmx.net", 
            'password1':"maxstinkt123", 
            'password2':"maxstinkt123", 
            'first_name': "Manni", 
            'last_name': "Mammut" 
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        
        self.assertTrue(form["username"], "TestsUse")
        #self.assertEqual(form["username"].errors, [force_text(User._meta.get_field('username'))])
        client = Client()
        self.assertTrue(client.session)
        client.login(username='TestUse', password='maxstinkt123')
        
        self.assertTrue(client.session)
        response = client.get("/create")
        self.assertEqual(response.status_code, 200)    

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