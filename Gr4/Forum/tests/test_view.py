from django.contrib.auth import get_user_model
from django.test import TestCase
from Forum.views import *

User = get_user_model




class test_home_view(TestCase): 

    def setUo(self):
        
        self.user = User.objects.create(username="TestUser", email="user@mp.com", password1="maxstinkt123", password2="maxstinkt123", first_name="Manni", last_name="Mammut" )


    def test_home_view(self):

        user = User(username ='Tim',email='test@gmx.de')
        user.set_password('some_234_wwf')
        user.save()
        
        #user_login = self.user.login(username="TestUser", password="maxstinkt123")
        loginuser = self.client.login(user)
        print(loginuser)
        self.assertTrue(loginuser)
        response = self.user.get("/")
        self.assertEqual(response.status_code, 302)