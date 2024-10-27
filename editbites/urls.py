from django.urls import path
from editbites import views

app_name = 'editbites'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    # path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('get_product_json/', views.get_product_json, name='get_product_json'),
]