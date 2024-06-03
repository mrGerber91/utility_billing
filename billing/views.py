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
    try:
        # Пытаемся получить существующие тарифы пользователя
        rates = Rates.objects.get(user=request.user)
    except Rates.DoesNotExist:
        # Если тарифов нет, создаем пустой объект для формы, но не сохраняем его сразу
        rates = Rates(user=request.user)
    
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
        form = UsageForm(request.POST, instance=previous_usage)
        if form.is_valid():
            current_usage = form.save(commit=False)
            current_usage.user = request.user
            current_usage.save(update_fields=['hot_water', 'cold_water', 'electricity', 'sewage'])
            return redirect('billing:show_bill')  # Переход к показу суммы счёта
    else:
        form = UsageForm(instance=previous_usage)  # Предзаполнение формы последними данными
    return render(request, 'billing/calculate_bill.html', {'form': form})

@login_required
def show_bill(request):
    # Получаем последние данные использования и тарифы для расчета счета
    try:
        current_usage = Usage.objects.filter(user=request.user).order_by('-id').first()
        rates = Rates.objects.get(user=request.user)

        # Расчет счета
        hot_water_bill = current_usage.hot_water * rates.hot_water
        cold_water_bill = current_usage.cold_water * rates.cold_water
        electricity_bill = current_usage.electricity * rates.electricity

        if current_usage.sewage:
            sewage_bill = current_usage.sewage * rates.sewage
        else:
            sewage_bill = (current_usage.hot_water + current_usage.cold_water) * rates.sewage

        bill = hot_water_bill + cold_water_bill + electricity_bill + sewage_bill

        context = {
            'bill': bill,
            'currency': rates.currency,
            'current_usage': current_usage  # Передаем последние использованные данные для отображения
        }

    except (Usage.DoesNotExist, Rates.DoesNotExist):
        # Если нет данных или тарифов, перенаправляем на страницу ввода тарифов или предыдущих данных
        return redirect('billing:setup_rates')

    return render(request, 'billing/show_bill.html', context)



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