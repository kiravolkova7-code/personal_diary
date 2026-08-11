from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("entries.urls", namespace="entries")),
    path("accounts/", include("users.urls", namespace="auth")),
]
