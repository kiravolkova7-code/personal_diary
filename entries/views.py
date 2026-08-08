from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Entry

class EntryListView(LoginRequiredMixin, ListView):
    """Отображает список всех записей текущего пользователя"""
    model = Entry
    template_name = 'entry_list.html'  # Путь к шаблону
    context_object_name = 'entries'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)  # Только свои записи


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entry_detail.html'

    def get_queryset(self):
        base_qs = super().get_queryset()
        return base_qs.filter(user=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry                     # <-- Добавлено: указываем модель
    fields = ['title', 'subject', 'content']  # <-- Добавлено: поля для формы
    template_name = "entry_form.html"
    success_url = reverse_lazy("entry-list") # Исправлено пространство имен

    def form_valid(self, form):
        print("Форма валидна! Пробуем сохранить...")
        form.instance.user = self.request.user
        result = super().form_valid(form)
        print(f"Сохранено под ID: {self.object.id}")
        return result


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    template_name = "entry_form.html"

    def get_queryset(self):
        # Ограничиваем доступ к редактированию своих записей
        base_qs = super().get_queryset()
        return base_qs.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление записи с подтверждением"""
    model = Entry
    success_url = '/'  # После удаления вернёмся на главную страницу
    template_name = 'entry_confirm_delete.html'

    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user  # Проверяем владельца
