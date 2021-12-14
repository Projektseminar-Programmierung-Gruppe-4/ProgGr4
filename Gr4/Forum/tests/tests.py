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

class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)



class VIEWTests(TestCase):
        
    def test_Forum_view(self):
        
        url = reverse("Forum.urls")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        


User = get_user_model
class UserTest(TestCase):
    def setUp(self):
        user_a = User(username ='Tim',email='test@gmx.de')
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password('some_234_wwf')
        user_a.save()
        print(user_a.id)

    def test_user_exists(self):
        user_count = User.objects.all().count
        self.assertEqual(user_count,1) 



class TestForumModel(TestCase):

    def test_model(self):
        title = Post.objects.create(title="Test Title")
        text = Post.objects.create(text="Test text ")

        self.assertEqual(str(title), "Test Title")
