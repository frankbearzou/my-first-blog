from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.


def post_list(request):
    pre_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = get_list_or_404(pre_posts)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'pk': pk, 'post': post})


def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)


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
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=pk)


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
