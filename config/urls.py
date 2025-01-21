from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurant.urls", "restaurant")),
    path("users/", include("users.urls", "users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
