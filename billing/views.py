# billing/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rates, Usage
from .forms import RatesForm, UsageForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
import logging
from django.core.exceptions import ValidationError
from django.contrib import messages

logger = logging.getLogger(__name__)

@login_required
def setup_rates(request):
    if request.method == 'POST':
        form = RatesForm(request.POST)
        if form.is_valid():
            rates = form.save(commit=False)
            rates.user = request.user
            rates.save()
            return redirect('input_previous_usage')
    else:
        form = RatesForm()
    return render(request, 'billing/setup_rates.html', {'form': form})

@login_required
def input_previous_usage(request):
    if request.method == 'POST':
        form = UsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.user = request.user
            usage.sewage = usage.hot_water + usage.cold_water  # Рассчитываем поле sewage
            usage.save()  # Сохраняем объект Usage
            return redirect('calculate_bill')
    else:
        form = UsageForm()
    return render(request, 'billing/input_previous_usage.html', {'form': form})


@login_required
def calculate_bill(request):
    if request.method == 'POST':
        current_usage_form = UsageForm(request.POST)
        if current_usage_form.is_valid():
            current_usage = current_usage_form.save(commit=False)
            current_usage.user = request.user
            previous_usage = Usage.objects.filter(user=request.user).order_by('-month').first()
            rates = Rates.objects.get(user=request.user)

            hot_water_bill = (current_usage.hot_water - previous_usage.hot_water) * rates.hot_water
            cold_water_bill = (current_usage.cold_water - previous_usage.cold_water) * rates.cold_water
            electricity_bill = (current_usage.electricity - previous_usage.electricity) * rates.electricity

            if current_usage.auto_calculate_sewage:  # Проверяем флаг автоматического рассчета водоотвода
                sewage = current_usage.hot_water + current_usage.cold_water
            else:
                sewage = current_usage.sewage  # Используем значение, если автоматический расчет отключен

            sewage_bill = (sewage - previous_usage.sewage) * rates.sewage if previous_usage.sewage is not None and sewage is not None else 0

            bill = hot_water_bill + cold_water_bill + electricity_bill + sewage_bill

            context = {'bill': bill, 'currency': rates.currency}
            current_usage.save()
            return render(request, 'billing/show_bill.html', context)
    else:
        current_usage_form = UsageForm()
    return render(request, 'billing/calculate_bill.html', {'form': current_usage_form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('home')
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
            return redirect('billing/setup_rates')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'billing/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        return redirect('billing:setup_rates')  # Убедитесь, что перенаправление идет на существующий маршрут
    else:
        return redirect('billing:register')  # Убедитесь, что перенаправление идет на существующий маршрут
