from django.urls import path
from . import views 
from .views import article_list, article_detail, add_article, delete_article, edit_article

app_name = 'artibites'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
    path('articles/<int:id>/edit/', views.edit_article, name='edit_article'),  
    path('articles/<int:id>/delete/', views.delete_article, name='delete_article'),  
    path('add/', views.add_article, name='add_article'),
]
