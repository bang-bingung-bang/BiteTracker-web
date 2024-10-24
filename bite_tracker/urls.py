"""
URL configuration for bite_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
from artibites import views  # Import views dari aplikasi artibites

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artibites/', include('artibites.urls')),  # URL untuk artibites
    path('', views.main_page, name='home'),  # Root URL mengarah ke main_page artibites
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('mybites/', include('MyBites.urls', namespace='MyBites')),
>>>>>>> 168a6b6940ec932cbc4404070213aa9edc007fa9
]


