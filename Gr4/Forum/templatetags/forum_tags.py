from django import template

from Forum.models import Postvotes

register = template.Library()

from Forum.models import Votes, Comment

@register.filter(name='comment_isliked')
def comment_isliked(pk, user):
    #comment = Comment.objects.get(pk=pk)
    user_id= user
    try:
        vote = Votes.objects.get(comment_id = pk, author_id = user_id)
    except:
        return False

    if vote.like == True:
        return True
    else:
        return False

@register.filter(name='comment_isdisliked')
def comment_isdisliked(pk, user):
    user_id= user
    try:
        vote = Votes.objects.get(comment_id = pk, author_id = user_id)
    except:
        return False

    if vote.dislike == True:
        return True
    else:
        return False


@register.filter(name='post_isliked')
def post_isliked(pk, user):
    #comment = Comment.objects.get(pk=pk)
    user_id= user
    try:
        vote = Postvotes.objects.get(post_id = pk, author_id = user_id)
    except:
        return False

    if vote.like == True:
        return True
    else:
        return False

@register.filter(name='post_isdisliked')
def post_isdisliked(pk, user):
    user_id= user
    try:
        vote = Postvotes.objects.get(post_id = pk, author_id = user_id)
    except:
        return False

    if vote.dislike == True:
        return True
    else:
        return False