from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import UserRegisterForm

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