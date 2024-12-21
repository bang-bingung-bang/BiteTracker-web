#main/views.py

from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import UserRegisterForm
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json

def show_main(request):
    return render(request, "main.html")

def register(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('main:login')
    context = {
        'form': form,
    }
    return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse('main:show_main'))
        else:
            messages.error(request, "User not found or incorrect password.")
    else:
        form = AuthenticationForm(request)
    
    context = {
        'form': form,
        'next': request.GET.get('next', '')
    }
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def login_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({
                        "status": "success",
                        "message": "Login successful!",
                        "username": user.username,
                        "is_admin": user.is_staff,
                    }, status=200)
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "Account is not active"
                    }, status=401)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid username or password"
                }, status=401)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=401)
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=401)

@csrf_exempt
def register_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserRegisterForm({
                'username': data['username'],
                'email': data['email'],
                'password1': data['password1'],
                'password2': data['password2'],
                'role': data['role']
            })
            
            if form.is_valid():
                user = form.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Registration successful!"
                }, status=200)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": dict(form.errors)
                }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=400)
