from django.urls import path
from main.views import register, login_user, show_main, logout_user, login_mobile, register_mobile

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # Mobile endpoints
    path('authen/login/', login_mobile, name='login_mobile'),
    path('authen/register/', register_mobile, name='register_mobile'),
    
]