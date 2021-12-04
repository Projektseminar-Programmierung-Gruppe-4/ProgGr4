from django.http import response
from django.test import TestCase
#from Forum.models import Forum
from django.utils import timezone
from django.urls import reverse
#from Forum.forms import Forum
# Create your tests here.


class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)



class VIEWTests(TestCase):
        
        def test_Forum_view(self):
            w = self.create_whatever()
            url = reverse("Forum.views")
            resp = self.client.get(url)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(w.title, resp.content)
