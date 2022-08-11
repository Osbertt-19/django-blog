from django import template
from ..models import Post
from django.utils.timezone import datetime


register = template.Library()


@register.inclusion_tag('draft_posts.html')
def show_draft_posts(author):
    draft_posts = Post.draft.filter(author=author)
    return {'posts': draft_posts}


@register.filter(name='full_status')
def full_status(status):
    if status == "DF":
        return "Draft"
    else:
        return "Published"
