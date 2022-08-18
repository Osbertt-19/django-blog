from django import template
from ..models import Post, Tag
from django.contrib.auth.models import User
from django.utils.timezone import datetime


register = template.Library()


@register.simple_tag()
def get_all_authors():
    return User.objects.all()


@register.simple_tag()
def get_all_tags():
    return Tag.objects.all()


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
