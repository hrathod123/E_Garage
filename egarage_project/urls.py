from django.contrib import admin
from django.urls import path, include
from core.admin import admin_site  # Import the instance from core/admin.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin_site.urls),  # Updated to point to your custom site
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)