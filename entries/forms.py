from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "subject", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control ckeditor"}),
        }

    subject = forms.ChoiceField(
        choices=Entry.SUBJECT_CHOICES, widget=forms.Select(attrs={"class": "form-select"}), label="Тема", required=True
    )
