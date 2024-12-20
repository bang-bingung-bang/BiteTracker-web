from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('main.urls')),
    path('', include('TrackerBites.urls')),
    path('artibites/', include('artibites.urls', namespace='artibites')),
    path('mybites/', include('MyBites.urls', namespace='MyBites')),
    path('sharebites/', include('sharebites.urls')),
    path('productbites/', include('editbites.urls', namespace='editbites')),
]