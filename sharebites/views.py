from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShareBites, Comment, Like
from .forms import ShareBitesForm, CommentForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers

@login_required
def show_main(request):
    posts = ShareBites.objects.all()
    liked_status = {}
    
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    context = {
        'posts': posts,
        'liked_posts': liked_posts,
    }
    return render(request, 'sharebites.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = ShareBitesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('sharebites:show_main')
    else:
        form = ShareBitesForm()
    
    return render(request, 'create_post_sharebites.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(ShareBites, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('sharebites:show_main')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(ShareBites, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('sharebites:show_main')  # Redirect to the post detail view or wherever you want
    else:
        form = CommentForm()

    return render(request, 'sharebites.html', {'form': form, 'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(ShareBites, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()  # Unlike the post
        liked = False
    else:
        liked = True

    response_data = {
        'liked': True,  
        'likes_count': post.likes.count()  # Get the updated likes count
    }

    # If it's an AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)

    return redirect('sharebites:show_main')

def show_xml(request):
    data = ShareBites.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ShareBites.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ShareBites.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ShareBites.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")