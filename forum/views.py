from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q

from .forms import CommentForm, PostForm
from .models import Community, Like, Post


def home(request):
    communities = Community.objects.all()
    return render(request, 'forum/home.html', {'communities': communities})


def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    posts = community.posts.select_related('author')
    return render(
        request,
        'forum/community_detail.html',
        {'community': community, 'posts': posts},
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author', 'community'), pk=pk
    )
    comments = post.comments.select_related('author')
    like_count = post.likes.count()
    user_liked = (
        request.user.is_authenticated
        and post.likes.filter(user=request.user).exists()
    )
    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'like_count': like_count,
        'user_liked': user_liked,
        'form': CommentForm(),
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(initial={'community': request.GET.get('community')})
    return render(request, 'forum/post_form.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        community_pk = post.community.pk
        post.delete()
        return redirect('community_detail', pk=community_pk)
    return render(request, 'forum/post_confirm_delete.html', {'post': post})


@login_required
@require_POST
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post_detail', pk=post.pk)


@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', pk=post.pk)    


def search(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).select_related('author', 'community')
    return render(request, 'forum/search_results.html', {
        'query': query,
        'posts': posts,
    })
