from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import views as auth_views


@method_decorator(csrf_protect, name='dispatch')
class RegisterView(generic.CreateView):
    """
    Представление для регистрации нового пользователя.
    Использует стандартный UserCreationForm.
    """
    template_name = 'registration/registration.html'
    form_class = RegistrationForm

    # Куда отправить пользователя ПОСЛЕ успешной регистрации
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Этот метод вызывается, когда форма валидна.
        Сначала сохраняется пользователь (super().form_valid),
        затем добавляется сообщение.
        """
        response = super().form_valid(form)  # Здесь происходит form.save()
        messages.success(self.request, f'Аккаунт {self.object.username} успешно создан!')
        return response


class CustomLoginView(auth_views.LoginView):
    """
    Кастомная вьюха входа, наследующаяся от стандартной LoginView
    """
    template_name = 'registration/login.html'  # Путь к вашему новому шаблону
    authentication_form = LoginForm  # Подключаем вашу форму с чекбоксом "Запомнить меня"
    success_url = reverse_lazy('entries:entry-list')
