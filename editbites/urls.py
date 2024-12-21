#Urls.py

from django.urls import path
from editbites import views

app_name = 'editbites'

urlpatterns = [
    # Web
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('get_product_json/', views.get_product_json, name='get_product_json'),
    path('add_products_from_fixtures/', views.add_products_from_fixtures, name='add_products_from_fixtures'),
    # Mobile
    path('mobile/create/', views.create_product_mobile, name='create_product_mobile'),
    path('mobile/<int:pk>/edit/', views.edit_product_mobile, name='edit_product_mobile'),
    path('mobile/<int:pk>/delete/', views.delete_product_mobile, name='delete_product_mobile'),
]