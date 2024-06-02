# billing/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Rates(models.Model):
    CURRENCY_CHOICES = (
        ('RUB', 'Российский рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hot_water = models.DecimalField(max_digits=10, decimal_places=2)
    cold_water = models.DecimalField(max_digits=10, decimal_places=2)
    electricity = models.DecimalField(max_digits=10, decimal_places=2)
    sewage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='RUB')

    def __str__(self):
        return f'Rates for {self.user}'

class Usage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField(default=date.today)
    hot_water = models.DecimalField(max_digits=10, decimal_places=2)
    cold_water = models.DecimalField(max_digits=10, decimal_places=2)
    electricity = models.DecimalField(max_digits=10, decimal_places=2)
    sewage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Поле водоотвода теперь необязательное
    auto_calculate_sewage = models.BooleanField(default=True)  # Флаг для автоматического расчета водоотвода

    def save(self, *args, **kwargs):
        if self.auto_calculate_sewage:
            self.sewage = self.hot_water + self.cold_water
        super().save(*args, **kwargs)

