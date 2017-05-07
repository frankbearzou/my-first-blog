from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.


def post_list(request):
    pre_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = get_list_or_404(pre_posts)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'pk': pk, 'post': post})


@login_required
def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'go_detail': pk})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=pk)


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def post_comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = CommentForm()
        return render(request, 'blog/post_comment_add.html', {'form': form})
    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
