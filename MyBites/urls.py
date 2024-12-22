from django.urls import path
from MyBites.views import show_main, show_xml, show_json, add_to_wishlist, view_wishlist, remove_from_wishlist, show_product_list, add_wishlist_flutter, view_wishlist_flutter, remove_flutter

app_name = 'MyBites'

urlpatterns = [
    path('mybites/', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('wishlist/', view_wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('products/', show_product_list, name='product_list'),
    path('flutter/add/<int:product_id>/', add_wishlist_flutter, name='add_wishlist_flutter'),
    path('flutter/view/', view_wishlist_flutter, name='view_wishlist_flutter'),
    path('flutter/remove/<int:id>/', remove_flutter, name="remove_flutter")
]
