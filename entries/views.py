from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import EntryForm
from .models import Entry


class EntryListView(LoginRequiredMixin, ListView):
    """Отображает список всех записей текущего пользователя"""

    model = Entry
    template_name = "entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        user_entries = Entry.objects.filter(user=self.request.user).order_by("-created_at")

        query = self.request.GET.get("q")
        if query:
            return user_entries.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

        return user_entries

    def get_context_data(self, **kwargs):
        """
        Добавляем текущий поисковый запрос в контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")

        from urllib.parse import urlencode

        params = self.request.GET.copy()
        params.pop("page", None)
        context["search_url_params"] = urlencode(params)

        return context


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "entry_detail.html"

    def get_queryset(self):
        base_qs = super().get_queryset()
        return base_qs.filter(user=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entry_form.html"
    success_url = reverse_lazy("entries:entry-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    template_name = "entry_form.html"
    form_class = EntryForm
    success_url = reverse_lazy("entries:entry-list")

    def get_queryset(self):
        base_qs = super().get_queryset()
        return base_qs.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление записи с подтверждением"""

    model = Entry
    success_url = reverse_lazy("entries:entry-list")
    template_name = "entry_confirm_delete.html"

    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user
