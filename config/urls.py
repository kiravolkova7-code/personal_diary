from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("entries.urls", namespace="entries")),
    path("api/", include("users.urls", namespace="api")),
    path('accounts/', include('django.contrib.auth.urls')),
]
