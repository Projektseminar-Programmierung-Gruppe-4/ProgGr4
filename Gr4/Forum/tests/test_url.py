from typing import Text
from django.contrib.auth.signals import user_logged_in
from django.forms.fields import EmailField
from django.http import response
from django.test import TestCase
#from Forum.models import Forum
from django.utils import timezone
from django.urls import reverse
#from Forum.forms import Forum
# Create your tests here.
from django.contrib.auth import get_user_model
from Forum.models import Post
from Forum.models import Comment


class URLTests(TestCase):
    
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_page(self):
        response = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    
        




