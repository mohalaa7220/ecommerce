from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/product/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
