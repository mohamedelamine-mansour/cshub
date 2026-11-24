from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Community, Post


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
    return render(request, 'forum/post_detail.html', {'post': post})


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