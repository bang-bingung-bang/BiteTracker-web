from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from artibites.models import Article  # Gunakan import absolut
from artibites.forms import ArticleForm  # Gunakan import absolut
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Import form custom
from django.contrib.auth.decorators import user_passes_test

@login_required(login_url='login')
def main_page(request):
    return render(request, 'main_page.html') #Halaman utama

# Menampilkan daftar artikel
def article_list(request):
    articles = Article.objects.all()  # Mengambil semua artikel dari database
    return render(request, 'article_list.html', {'articles': articles})

# Menampilkan detail artikel
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)  # Mendapatkan artikel berdasarkan ID, atau 404 jika tidak ada
    return render(request, 'article_detail.html', {'article': article})

# Fungsi untuk memeriksa apakah user adalah admin
def is_admin(user):
    return user.is_staff

# Menambah artikel baru (hanya admin yang bisa mengakses)
@user_passes_test(is_admin)
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirect ke daftar artikel setelah berhasil menyimpan
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})

@user_passes_test(is_admin)
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})

# Hapus artikel
@user_passes_test(is_admin)
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'delete_article.html', {'article': article})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_staff']  # Set is_staff sesuai pilihan
            user.save()
            messages.success(request, 'Akun Anda berhasil dibuat!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')  # Ubah dari 'main:show_main' ke 'main_page'

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')  # Mengarahkan kembali ke halaman login