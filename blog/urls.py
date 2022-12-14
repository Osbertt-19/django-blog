from django.urls import path
from . import views, feeds

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<str:author>/', views.index, name='author'),
    path('tag/<str:tag>/', views.index, name='tag'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/share/', views.post_share, name='post_share'),
    path('feed/', feeds.LatestPostsFeed(), name='post_feed'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
