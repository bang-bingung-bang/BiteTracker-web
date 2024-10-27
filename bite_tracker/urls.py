from django.contrib import admin
from django.urls import include, path
from artibites import views  # Import views dari aplikasi artibites
from main import views #Import views dari main


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('mybites/', include('MyBites.urls', namespace='MyBites')),
]
