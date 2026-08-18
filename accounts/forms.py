from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class BootstrapFormMixin:
    """Har bir formaga avtomatik ravishda Bootstrap CSS klasslarini qo'shadi."""
    def _apply_bootstrap_classes(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-check-input').strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-select').strip()
            else:
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' form-control').strip()


class PatientRegisterForm(BootstrapFormMixin, UserCreationForm):
    """Bemor sifatida ro'yxatdan o'tish formasi."""
    first_name = forms.CharField(label="Ism", max_length=150, required=True)
    last_name = forms.CharField(label="Familiya", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Telefon raqami", max_length=20, required=True,
                             widget=forms.TextInput(attrs={'placeholder': '+998 90 123 45 67'}))
    birth_date = forms.DateField(label="Tug'ilgan sana", required=False,
                                  widget=forms.DateInput(attrs={'type': 'date'}))
    avatar = forms.ImageField(label="Profil rasmi (ixtiyoriy)", required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'birth_date',
                   'avatar', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PATIENT
        if commit:
            user.save()
        return user


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label="Foydalanuvchi nomi", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'address', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()
