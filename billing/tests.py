from django.test import TestCase
from django.contrib.auth.models import User
from .models import Rates, Usage
from .forms import RatesForm, UsageForm

class RatesModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_rates_creation(self):
        rates = Rates.objects.create(
            user=self.user,
            hot_water=10.5,
            cold_water=5.5,
            electricity=20.0,
            sewage=2.5,
            currency='RUB'
        )
        self.assertEqual(rates.user.username, 'testuser')
        self.assertEqual(rates.hot_water, 10.5)

class UsageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_usage_creation(self):
        usage = Usage.objects.create(
            user=self.user,
            hot_water=15.0,
            cold_water=10.0,
            electricity=30.0,
            sewage=5.0
        )
        self.assertEqual(usage.user.username, 'testuser')
        self.assertEqual(usage.hot_water, 15.0)

class FormsTest(TestCase):

    def test_rates_form(self):
        form_data = {
            'hot_water': 10.5,
            'cold_water': 5.5,
            'electricity': 20.0,
            'sewage': 2.5,
            'currency': 'RUB'
        }
        form = RatesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_usage_form(self):
        form_data = {
            'month': '2024-05-27',
            'hot_water': 15.0,
            'cold_water': 10.0,
            'electricity': 30.0,
            'sewage': 5.0
        }
        form = UsageForm(data=form_data)
        self.assertTrue(form.is_valid())
