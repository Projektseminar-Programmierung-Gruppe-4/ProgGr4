from django import template

register = template.Library()

from Forum.models import Votes

def is_liked(pk):
    return