# billing/forms.py
from django import forms
from .models import Rates, Usage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class RatesForm(forms.ModelForm):
    class Meta:
        model = Rates
        fields = ['hot_water', 'cold_water', 'electricity', 'sewage', 'currency']
        widgets = {
            'currency': forms.Select(choices=Rates.CURRENCY_CHOICES)
        }

class UsageForm(forms.ModelForm):
    month = forms.DateField(widget=forms.SelectDateWidget())
    sewage = forms.DecimalField(label='Sewage', required=False)  # Поле водоотвода стало необязательным
    auto_calculate_sewage = forms.BooleanField(label='Auto calculate sewage', required=False, initial=True)  # Добавлен чекбокс для указания, нужно ли автоматически рассчитывать водоотвод

    class Meta:
        model = Usage
        fields = ['month', 'hot_water', 'cold_water', 'electricity', 'sewage', 'auto_calculate_sewage']  # Добавлено новое поле auto_calculate_sewage

    def clean(self):
        cleaned_data = super().clean()
        auto_calculate_sewage = cleaned_data.get('auto_calculate_sewage')
        if auto_calculate_sewage:
            hot_water = cleaned_data.get('hot_water')
            cold_water = cleaned_data.get('cold_water')
            cleaned_data['sewage'] = hot_water + cold_water
        return cleaned_data
class UserRegistrationForm(UserCreationForm):
    class Meta:
        captcha = CaptchaField()
        model = User
        fields = ['username', 'password1', 'password2']