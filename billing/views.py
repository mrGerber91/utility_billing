from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rates, Usage
from .forms import RatesForm, UsageForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
import logging
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

logger = logging.getLogger(__name__)

@login_required
def setup_rates(request):
    # Пытаемся получить существующие тарифы пользователя, иначе создаем новый объект
    rates, created = Rates.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = RatesForm(request.POST, instance=rates)
        if form.is_valid():
            form.save()
            return redirect('billing:input_previous_usage')
    else:
        form = RatesForm(instance=rates)

    return render(request, 'billing/setup_rates.html', {'form': form})

@login_required
def input_previous_usage(request):
    # Создаем новую форму для ввода предыдущего потребления
    if request.method == 'POST':
        form = UsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.user = request.user
            usage.save()
            return redirect('billing:calculate_bill')
    else:
        form = UsageForm()

    return render(request, 'billing/input_previous_usage.html', {'form': form})

@login_required
def calculate_bill(request):
    previous_usage = Usage.objects.filter(user=request.user).order_by('-month').first()
    if request.method == 'POST':
        form = UsageForm(request.POST, instance=previous_usage if previous_usage else None)
        if form.is_valid():
            current_usage = form.save(commit=False)
            current_usage.user = request.user
            current_usage.save()
            return redirect('billing:show_bill')
    else:
        form = UsageForm()

    return render(request, 'billing/calculate_bill.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('billing:profile')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  # Автоматический вход после регистрации
                return redirect('billing:profile')
        else:
            form = UserRegistrationForm()
        return render(request, 'billing/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('billing:setup_rates')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'billing/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        # Проверяем, есть ли данные о тарифах
        if Rates.objects.filter(user=request.user).exists():
            return redirect('billing:calculate_bill')
        else:
            return redirect('billing:setup_rates')
    else:
        return redirect('billing:register')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно для поддержания сессии пользователя после смены пароля
            messages.success(request, 'Your password was successfully updated!')
            return redirect('billing:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'billing/change_password.html', {'form': form})

@login_required
def update_profile(request):
    # Пример обновления профиля, зависит от того, как вы хотите обрабатывать данные
    return render(request, 'billing/update_profile.html')

@login_required
def profile(request):
    return render(request, 'billing/profile.html')