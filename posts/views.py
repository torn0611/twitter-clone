# from typing_extensions import Required
from django import forms
from django.http.response import HttpResponseBase, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.urls import reverse
# Create your views here.

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts', args=[str(pk)]))



def index(request):
    # if the method is POST
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
    # If the form is valid
        if form.is_valid():
            #yes, save
            form.save()
          # Redirect to home
            return HttpResponseRedirect('/')

        else:
            # no, Show Error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]
    # Show
    return render(request, 'posts.html', {'posts': posts})

def likes(request, post_id):
    print(post_id)
    likedTweet = Post.objects.get(id=post_id)
    likedTweet.like_count += 1
    likedTweet.save()
    return HttpResponseRedirect("/")


def delete(request, post_id):
    # Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    posts = Post.objects.get(id = post_id)
    if request.method == 'GET':
        posts = Post.objects.get(id=post_id)
        return render(request, "edit.html", {"posts": posts})
    if request.method == 'POST':
        editposts = Post.objects.get(id=post_id)
        form = PostForm(request.POST, request.FILES, instance=editposts)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Not Valid")
