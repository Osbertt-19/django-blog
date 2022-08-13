from django.shortcuts import render, redirect
from .models import Post, Comment, Tag
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.db.models import Count


def index(request, author=None, tag=None):
    post_list = Post.published.all()
    filter_ = ''
    if tag:
        post_list = post_list.filter(tags__name__in=[tag])
        filter_ = f'with #{tag} tag'
    if author:
        post_list = post_list.filter(author__username=author)
        filter_ = f'of {author}'
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
        'posts': posts,
        'filter': filter_,
        'all_posts': post_list,
    }

    return render(request, 'index.html', context)


@login_required(login_url='login')
def post_create(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.user
        body = request.POST['body']
        status = request.POST['status']
        tags = request.POST['tags'].split(',')
        post = Post.objects.create(title=title, author=author, body=body, status=status,)
        for tag_name in tags:
            tag = Tag.objects.create(name=tag_name, slug=slugify(tag_name))
            tag.save()
            post.tags.add(tag)
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

    # List of similar posts
    post_tags_names = post.tags.values_list('name', flat=True)
    similar_posts = Post.published.filter(tags__name__in=post_tags_names).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')

    user_can_edit_del_post = post.author == request.user
    context = {
        'post': post,
        'user_can_edit_del_post': user_can_edit_del_post,
        'similar_posts': similar_posts,
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
        selected_post.tags.clear()
        tags = request.POST['tags'].split(',')
        for tag_name in tags:
            tag = Tag.objects.create(name=tag_name, slug=slugify(tag_name))
            tag.save()
            selected_post.tags.add(tag)
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
    sent = False
    to = None
    shared_post = Post.objects.get(pk=pk)
    if request.method == "POST":
        url = request.build_absolute_uri(shared_post.get_absolute_url())
        from_ = request.user
        to = request.POST['to']
        comment = request.POST['comment']
        subject = f"{from_} recommends you to read {shared_post.title} by {shared_post.author}"
        message = f"Read {shared_post.title} by {shared_post.author} at {url} \n" \
                  f"{from_} : {comment}"
        send_mail(subject, message, 'minhtetnaing25mhn@gmail.com', [to])
        sent = True

    context = {
        'post': shared_post,
        'sent': sent,
        'to': to,
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
