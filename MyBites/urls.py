from django.urls import path
from MyBites.views import show_main, show_xml, show_json, add_to_wishlist, view_wishlist, remove_from_wishlist, show_product_list

app_name = 'MyBites'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('wishlist/', view_wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('products/', show_product_list, name='product_list'),
]
