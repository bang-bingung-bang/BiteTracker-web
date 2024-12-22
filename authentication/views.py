#views.py

import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            user = User.objects.get(username=username)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "email": user.email,
                "role": user.is_staff,
                "user_id": user.pk,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

from django.contrib.auth import logout as auth_logout
@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Ambil data dari POST request
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            role = request.POST.get('role', 'member')

            # Validasi input
            if not all([username, email, password1, password2]):
                return JsonResponse({
                    "status": False,
                    "message": "Semua field harus diisi!"
                }, status=400)

            if password1 != password2:
                return JsonResponse({
                    "status": False,
                    "message": "Password tidak cocok!"
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username sudah digunakan!"
                }, status=400)

            # Buat user baru
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            
            # Set role
            user.is_staff = (role == 'admin')
            user.save()
            
            return JsonResponse({
                "status": True,
                "message": "Register berhasil!",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.is_staff,
                }
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Registration failed: {str(e)}"
            }, status=400)

    return JsonResponse({
        "status": False,
        "message": "Method not allowed."
    }, status=405)