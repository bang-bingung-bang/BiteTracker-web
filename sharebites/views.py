from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShareBites, Comment, Like
from .forms import ShareBitesForm, CommentForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

# @login_required
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

@csrf_exempt
# @login_required
def delete_post(request, pk):
    if request.method == 'DELETE':
        post = get_object_or_404(ShareBites, pk=pk)
        post.delete()
        return JsonResponse({'status': 'success'}, status=204)  # Return success response with 204 status
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
            # Return JSON response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'success': True,
                    'comment': {
                        'username': comment.user.username,
                        'content': comment.content
                    }
                }
                return JsonResponse(response_data)
            return redirect('sharebites:show_main')  # Redirect for normal requests
    # Return errors if not valid
    return JsonResponse({'success': False, 'errors': form.errors})

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

@csrf_exempt
def create_post_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Ambil user (gunakan default jika tidak ada)
            user = User.objects.get(id=data['user_id']) if 'user_id' in data else None

            new_post = ShareBites.objects.create(
                user=user,
                title=data['title'],
                content=data['content'],
                image=data['image'],
                calorie_content=data['calorie_content'],
                sugar_content=data['sugar_content'],
                diet_type=data['diet_type']
            )

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

@csrf_exempt
def add_comment_flutter(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = ShareBites.objects.get(pk=post_id)
            user = User.objects.get(id=data.get('user_id', 2))  # Default user_id 2
            
            comment = Comment.objects.create(
                post=post,
                user=user,
                content=data['content']
            )
            
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'id': comment.id,
                    'user': comment.user.username,
                    'content': comment.content
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def get_comments_flutter(request, post_id):
    try:
        comments = Comment.objects.filter(post_id=post_id)
        comments_data = [{
            'id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'user_id': comment.user.id
        } for comment in comments]
        
        return JsonResponse(comments_data, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def like_post_flutter(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)
            post = ShareBites.objects.get(id=post_id)
            
            like, created = Like.objects.get_or_create(post=post, user=user)
            
            if not created:
                # User already liked the post, so unlike it
                like.delete()
                liked = False
            else:
                # New like
                liked = True
            
            return JsonResponse({
                'status': 'success',
                'liked': liked,
                'likes_count': post.likes.count()
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)
            
        except ShareBites.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Post not found'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@csrf_exempt
def get_like_status(request, post_id):
    try:
        post = ShareBites.objects.get(pk=post_id)
        user_id = request.GET.get('user_id')
        
        if user_id:
            user = User.objects.get(id=user_id)
            is_liked = Like.objects.filter(post=post, user=user).exists()
        else:
            is_liked = False
            
        return JsonResponse({
            'status': 'success',
            'is_liked': is_liked,
            'likes_count': post.likes.count()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def toggle_like(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if not user_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'User ID is required'
                }, status=400)
                
            user = User.objects.get(id=user_id)
            post = ShareBites.objects.get(pk=post_id)
            
            like, created = Like.objects.get_or_create(post=post, user=user)
            
            if not created:
                like.delete()
                is_liked = False
            else:
                is_liked = True
                
            return JsonResponse({
                'status': 'success',
                'liked': is_liked,
                'likes_count': post.likes.count()
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)
            
        except ShareBites.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Post not found'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)