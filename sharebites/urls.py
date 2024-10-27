from django.urls import path
from . import views

app_name = 'sharebites'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('create/', views.create_post, name='create_post_sharebites'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
]
