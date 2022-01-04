from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from Forum.models import Post


class PostModelTest(TestCase):

    def test_title(self):

        post  = Post(title="Hallo Welt")
        self.assertEqual(str(post), post.title)
    
    


class TestForumModel(TestCase):

    def test_model(self):
        title = Post.objects.create(title="Test Title")
        voteCount = Post.objects.create(voteCount= 2)
        #text = Post.objects.create(text="Test text ")

        self.assertEqual(str(title), "Test Title")
        #self.assertEqual(int(voteCount),2 )




