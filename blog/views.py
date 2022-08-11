from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
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
        status = request.POST['status']
        post = Post.objects.create(title=title, author=author, body=body, status=status)
        post.save()
        return redirect('index')
    else:

        return render(request, 'post_create.html')


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        body = request.POST['body']
        if request.user.is_authenticated:
            commenter = User.objects.get(username=request.user.username)
            comment = Comment.objects.create(body=body, commenter=commenter, post=post)
            comment.save()
        else:
            messages.info(request, 'U need to log in to comment')

    user_can_edit_del_post = post.author == request.user
    context = {
        'post': post,
        'user_can_edit_del_post': user_can_edit_del_post
    }
    return render(request, 'post_detail.html', context)


@login_required(login_url='login')
def post_edit(request, pk):
    selected_post = Post.objects.get(pk=pk)
    if selected_post.author == request.user:
        pass
    if request.method == "POST":
        selected_post.title = request.POST['title']
        selected_post.author = request.user
        selected_post.body = request.POST['body']
        selected_post.status = request.POST['status']
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
    if deleted_post.author == request.user:
        pass
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
        return redirect('index')
    else:
        return render(request, 'logout.html')
