from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def index(request):
    posts = Post.objects.all
    context = {
        'posts': posts
    }

    return render(request, 'index.html', context)


@login_required(login_url='login')
def post_create(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.user
        body = request.POST['body']
        post = Post.objects.create(title=title, author=author, body=body)
        post.save()
        return redirect('index')
    else:

        return render(request, 'post_create.html')


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post_detail.html', context)


@login_required(login_url='login')
def post_edit(request, pk):
    selected_post = Post.objects.get(pk=pk)
    if request.method == "POST":
        title = request.POST['title']
        author = request.user
        body = request.POST['body']
        selected_post.title = title
        selected_post.author = author
        selected_post.body = body
        selected_post.save()
        return redirect('post_detail', selected_post.pk)
    else:
        context = {
            'post': selected_post
        }
        return render(request, 'post_edit.html', context)


@login_required(login_url='login')
def post_delete(request, pk):
    deleted_post = Post.objects.get(pk=pk)
    if request.method == "POST":
        deleted_post.delete()
        return redirect('index')
    else:
        context = {
            'post': deleted_post
        }
        return render(request, 'post_delete.html', context)


@login_required(login_url='login')
def post_share(request, pk):
    shared_post = Post.objects.get(pk=pk)
    if request.method == "POST":
        url = request.build_absolute_uri(shared_post.get_absolute_url())
        name = request.POST['name']
        to = request.POST['to']
        comment = request.POST['comment']
        subject = f"{name} recommends you to read {shared_post.title} by {shared_post.author}"
        message = f"Read {shared_post.title} by {shared_post.author} at {url} " f" {name} : {comment}"
        send_mail(subject, message, 'minhtetnaing25mhn@gmail.com', [to])
        return redirect('index')
    else:
        context = {
            'shared_post': shared_post
        }
        return render(request, 'post_share.html', context)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('index')
        else:
            messages.info(request, 'Passwords not Matched')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_login = auth.authenticate(username=username, password=password)
        if user_login is not None:
            auth.login(request, user_login)
            return redirect('index')
        else:
            messages.info(request, 'There is no such user')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('login')
    else:
        return render(request, 'logout.html')
