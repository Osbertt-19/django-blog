from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostAPIView.as_view()),
    path('comments/', views.CommentAPIView.as_view()),
    path('tags/', views.TagAPIView.as_view()),
]
