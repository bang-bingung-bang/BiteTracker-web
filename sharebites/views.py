from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShareBites, Comment, Like
from .forms import ShareBitesForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# @login_required
def show_main(request):
    posts = ShareBites.objects.all()
    liked_status = {}
    
    if request.user.is_authenticated:
        liked_status = {
            post.pk: post.likes.filter(user=request.user).exists() for post in posts
        }
    
    context = {
        'posts': posts,
        'liked_status': liked_status,
    }
    return render(request, 'sharebites.html', {'posts': posts})

# @login_required
def create_post(request):
    if request.method == 'POST':
        form = ShareBitesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            # Dapatkan nilai dari dropdown
            calorie_content = form.cleaned_data.get('calorie_content')
            sugar_content = form.cleaned_data.get('sugar_content')
            diet_type = form.cleaned_data.get('diet_type')

            # Simpan hanya jika bukan 'none'
            if calorie_content != 'none':
                post.calorie_content = calorie_content
            else:
                post.calorie_content = None  # Atau bisa dibiarkan saja jika field nullable

            if sugar_content != 'none':
                post.sugar_content = sugar_content
            else:
                post.sugar_content = None  # Atau bisa dibiarkan saja jika field nullable

            if diet_type != 'none':
                post.diet_type = diet_type
            else:
                post.diet_type = None  # Atau bisa dibiarkan saja jika field nullable

            post.save()
            return redirect('sharebites:show_main')
    else:
        form = ShareBitesForm()
    
    return render(request, 'create_post_sharebites.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(ShareBites, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('sharebites:show_main')

# @login_required
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

# @login_required
def like_post(request, post_id):
    post = get_object_or_404(ShareBites, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()  # Unlike the post

    response_data = {
        'liked': created,  # True if liked, False if unliked
        'likes_count': post.likes.count()  # Get the updated likes count
    }

    # If it's an AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)

    return redirect('sharebites:show_main')


