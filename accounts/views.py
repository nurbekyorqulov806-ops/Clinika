from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import PatientRegisterForm, LoginForm, ProfileUpdateForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:redirect_after_login')

    if request.method == 'POST':
        form = PatientRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('accounts:redirect_after_login')
    else:
        form = PatientRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:redirect_after_login')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz.")
            return redirect('accounts:redirect_after_login')
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('home')


@login_required
def redirect_after_login(request):
    user = request.user
    if user.is_admin_role:
        return redirect('dashboard:admin_dashboard')
    if user.is_doctor_role:
        return redirect('appointments:doctor_dashboard')
    return redirect('appointments:patient_dashboard')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
