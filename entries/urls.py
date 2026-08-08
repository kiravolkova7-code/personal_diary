from django.urls import path

from .apps import EntriesConfig
from .views import (
    EntryListView,
    EntryDetailView,
    EntryCreateView,
    EntryUpdateView,
    EntryDeleteView
)


app_name = EntriesConfig.name

urlpatterns = [
    path('', EntryListView.as_view(), name='entry-list'),
    path('create/', EntryCreateView.as_view(), name='entry-create'),
    path('<int:pk>/', EntryDetailView.as_view(), name='entry-detail'),
    path('<int:pk>/update/', EntryUpdateView.as_view(), name='entry-update'),
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name='entry-delete'),
]