from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from artibites.models import Article  
from artibites.forms import ArticleForm  
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  
from django.contrib.auth.decorators import user_passes_test

@login_required
def show_main(request):
    return render(request, 'main/main.html')

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
            return redirect('artibites:article_list')   # Redirect ke daftar artikel setelah berhasil menyimpan
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
            return redirect('artibites:article_detail', id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})

# Hapus artikel
@user_passes_test(is_admin)
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('artibites:article_list')

    return render(request, 'artibites/delete_article.html', {'article': article})   
