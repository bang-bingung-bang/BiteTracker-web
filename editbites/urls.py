from django.urls import path
from . import views

app_name = 'editbites'

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('json/', views.get_products_json, name='get_products_json'),
]