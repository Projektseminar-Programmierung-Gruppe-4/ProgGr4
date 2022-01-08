from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from django.urls.base import reverse
from Forum.models import Post
from Forum.views import *



class testPost(TestCase):

    def create_post_model(self, title="testone", text="onlytest"):
        return Post.objects.create(title=title, text=text)

    def test_post_creat(self):

        w = self.create_post_model()
        self.assertTrue(isinstance(w, Post))
        self.assertEqual(w.__str__(), w.title)
    

class testComment(TestCase):

    def create_comment_model(self, text="testtext"):
        return Comment.objects.create( text=text)
    
    def test_comment_create(self):
        comment_create = self.create_comment_model()
        self.assertTrue(isinstance(comment_create, Comment))
        self.assertEqual(comment_create.__str__(), comment_create.text)
        



class PostModelTest(TestCase):

    def test_title(self):

        post  = Post(
        title="Hallo Welt",
        text="test body",
        voteCount=2,
        created_date = "2022-01-04 14:58:25.86806+00"
        )

        self.assertEqual(post.title, "Hallo Welt")
        self.assertEqual(post.text, "test body")
        self.assertEqual(post.voteCount, 2)
    
    


class TestForumModel(TestCase):

    def test_model(self):
        title = Post.objects.create(title="Test Title")
        voteCount = Post.objects.create(voteCount= 2)
        

        self.assertEqual(str(title), "Test Title")
        #self.assertEqual(int(voteCount),2 )





