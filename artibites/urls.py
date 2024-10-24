from django.urls import path
from . import views  # Pastikan Anda mengimpor views
from .views import main_page, article_list, article_detail, add_article, register, logout_user, login_user

urlpatterns = [
    path('', views.main_page, name='main_page'),  # Pastikan ada URL dengan nama 'main_page'
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
    path('articles/<int:id>/edit/', views.edit_article, name='edit_article'),  # URL edit artikel
    path('articles/<int:id>/delete/', views.delete_article, name='delete_article'),  # URL hapus artikel
    path('add/', views.add_article, name='add_article'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
