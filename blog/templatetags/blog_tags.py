from django import template
from ..models import Post
from django.utils.timezone import datetime


register = template.Library()
