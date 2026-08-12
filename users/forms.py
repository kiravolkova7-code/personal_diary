from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=" ",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Придумайте пароль*", "aria-label": "Пароль", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label=" ",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Повторите пароль*", "aria-label": "Подтверждение пароля", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "email", "phone", "city", "avatar")  # avatar оставляем здесь для сохранения

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Имя*", "aria-label": "Имя", "class": "form-control"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email*", "aria-label": "Электронная почта", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Телефон (+7 999 999 99 99)",
                    "aria-label": "Телефон",
                    "class": "form-control",
                    "type": "tel",
                }
            ),
            "city": forms.TextInput(attrs={"placeholder": "Город", "aria-label": "Город", "class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),  # Стилизуем кнопку выбора файла
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.ClearableFileInput):  # У аватара оставим стандартный вид кнопки
                field.label = ""

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают.")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Кастомная форма входа
    """

    username = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email*",
                "aria-label": "Электронная почта",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль*",
                "aria-label": "Пароль",
                "autocomplete": "current-password",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
