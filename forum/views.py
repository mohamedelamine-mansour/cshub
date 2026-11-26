from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm, ReportForm
from .models import Community, Like, Post, Report

POSTS_PER_PAGE = 10


def posts_with_counts():
    return Post.objects.select_related('author', 'community').annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
    )


def paginate(request, queryset):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    return paginator.get_page(request.GET.get('page'))


def home(request):
    communities = Community.objects.all()
    page = paginate(request, posts_with_counts())
    return render(request, 'forum/home.html', {
        'communities': communities,
        'page': page,
    })


def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    page = paginate(request, posts_with_counts().filter(community=community))
    return render(request, 'forum/community_detail.html', {
        'community': community,
        'page': page,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    if query:
        posts = posts_with_counts().filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    page = paginate(request, posts)
    return render(request, 'forum/search_results.html', {
        'query': query,
        'page': page,
        'querystring': urlencode({'q': query}) if query else '',
    })


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





@login_required
def report_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            already = Report.objects.filter(
                reporter=request.user, post=post, is_handled=False
            ).exists()
            if already:
                messages.info(request, 'You already reported this post. The admin will review it.')
            else:
                report = form.save(commit=False)
                report.reporter = request.user
                report.post = post
                report.save()
                messages.success(request, 'Thank you. Your report was sent to the admin.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = ReportForm()
    return render(request, 'forum/report_form.html', {'form': form, 'post': post})



def rules(request):
    return render(request, 'forum/rules.html')    



