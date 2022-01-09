from django.contrib.auth import get_user_model
from django.db.models.query_utils import select_related_descend
from django.test.testcases import TestCase
from django.urls.base import reverse
from Forum.models import Post
from Forum.views import *



class testPost(TestCase):

    def create_post_model(self, title="testone", text="onlytest"):
        return Post.objects.create(title=title, text=text)

    def test_post_creat(self):

        test_post_create = self.create_post_model()
        self.assertTrue(isinstance(test_post_create, Post))
        self.assertEqual(test_post_create.__str__(), test_post_create.title)
        
    

class testComment(TestCase):

    def create_comment_model(self, text="testtext"):
        return Comment.objects.create( text=text)
    
    def test_comment_create(self):
        comment_create = self.create_comment_model()
        self.assertTrue(isinstance(comment_create, Comment))
        self.assertEqual(comment_create.__str__(), comment_create.text)
        
class testSubComment(TestCase):

    def create_subcomment_model(self, text="testsubcomment"):
        return Subcomment.objects.create( text=text)
    
    def test_subcomment_create(self):
        subcomment_create = self.create_subcomment_model()
        self.assertTrue(isinstance(subcomment_create, Subcomment))
        self.assertEqual(subcomment_create.__str__(), subcomment_create.text)

class testVotes(TestCase):

    def votes_model(self, id=1 ,like=True ,dislike=False):
        return Votes.objects.create( id=id, like=like, dislike=dislike)
    
    def test_votes(self):
        votes_create = self.votes_model()
        self.assertTrue(isinstance(votes_create, Votes))
        self.assertEqual(votes_create.__str__(), votes_create.id)

class testPostVotes(TestCase):

    def post_votes_model(self, id=1 ,like=True ,dislike=False):
        return Postvotes.objects.create( id=id, like=like, dislike=dislike)
    
    def test_votes(self):
        postvotes_create = self.post_votes_model()
        self.assertTrue(isinstance(postvotes_create, Postvotes))
        self.assertEqual(postvotes_create.__str__(), postvotes_create.id)

class testSubCommentVotes(TestCase):

    def subcomment_votes_model(self, id=1 ,like=True ,dislike=False):
        return Subcommentvotes.objects.create( id=id, like=like, dislike=dislike)
    
    def test_subcomment_votes(self):
        subcomment_votes_create = self.subcomment_votes_model()
        self.assertTrue(isinstance(subcomment_votes_create, Subcommentvotes))
        self.assertEqual(subcomment_votes_create.__str__(), subcomment_votes_create.id)


class testDepartment(TestCase):

    def create_department_model(self, name="test department"):
        return Department.objects.create( name=name)
    
    def test_department(self):
        department_create = self.create_department_model()
        self.assertTrue(isinstance(department_create, Department))
        self.assertEqual(department_create.__str__(), department_create.name)





class PostModelTest(TestCase):

    def test_post_model(self):

        post  = Post(
        title="Hallo Welt",
        text="test body",
        voteCount=2,
        created_date = "2022-01-04 14:58:25.86806+00"
        )

        self.assertEqual(post.title, "Hallo Welt")
        self.assertEqual(post.text, "test body")
        self.assertEqual(post.voteCount, 2)
    
class CommentModelTest(TestCase):

     def test_comment_model(self):

        comment = Comment(
        text= "TestText",
        voteCount = 2
         )   

        self.assertEqual(comment.text, "TestText")
        self.assertEqual(comment.voteCount, 2)


class SubCommentModelTest(TestCase):

     def test_subcomment_model(self):

        sub_comment = Subcomment(
        text= "TestSubcomment",
        voteCount = 1
         )   

        self.assertEqual(sub_comment.text, "TestSubcomment")
        self.assertEqual(sub_comment.voteCount, 1)


class VotesModelTest(TestCase):

    def test_like_model(self):

        votes = Votes(
        like=True,
        dislike = False
         )   

        self.assertEqual(votes.like, True)
        self.assertEqual(votes.dislike, False)
    
    def test_dislike_model(self):

        votes = Votes(
        like=False,
        dislike = True
        )   

        self.assertEqual(votes.like, False)
        self.assertEqual(votes.dislike, True)

    #Post Votes  
    def test_post_like_model(self):

        votes = Postvotes(
        like=True,
        dislike = False
         )   

        self.assertEqual(votes.like, True)
        self.assertEqual(votes.dislike, False)
    
    def test_post_dislike_model(self):

        votes = Postvotes(
        like=False,
        dislike = True
        )   

        self.assertEqual(votes.like, False)
        self.assertEqual(votes.dislike, True)

    #subcomment votes

    def test_subcomment_like_model(self):

        votes = Subcommentvotes(
        like=True,
        dislike = False
         )   

        self.assertEqual(votes.like, True)
        self.assertEqual(votes.dislike, False)
    
    def test_subcomment_dislike_model(self):

        votes = Subcommentvotes(
        like=False,
        dislike = True
        )   

        self.assertEqual(votes.like, False)
        self.assertEqual(votes.dislike, True)





class DepartmentTest(TestCase):

    def test_department_model(self):

        department = Department(
        name = "IT"
        )
        self.assertEqual(department.name, "IT")



