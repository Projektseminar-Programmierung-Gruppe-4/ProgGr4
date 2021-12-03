from django import template

register = template.Library()

from Forum.models import Votes, Comment

@register.filter(name='is_liked')
def is_liked(pk, user):
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

@register.filter(name='is_disliked')
def is_disliked(pk, user):
    user_id= user
    try:
        vote = Votes.objects.get(comment_id = pk, author_id = user_id)
    except:
        return False
        
    if vote.dislike == True:
        return True
    else:
        return False