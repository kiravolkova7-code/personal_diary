from django.urls import path
from django.contrib.auth import views as auth_views

from .apps import UsersConfig
from .views import RegisterView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    # Вход и выход через стандартные представления со своими шаблонами
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Ваша кастомная регистрация
    path('register/', RegisterView.as_view(), name='register'),
]