from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'df', 'Draft'
        PUBLISHED = 'pb', 'Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique_for_date=publish)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class meta:
        ordering=['-publish',]
