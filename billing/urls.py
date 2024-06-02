# billing/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import RatesViewSet, UsageViewSet

app_name = 'billing'

router = DefaultRouter()
router.register(r'rates', RatesViewSet)
router.register(r'usage', UsageViewSet)

urlpatterns = [
    path('setup_rates/', views.setup_rates, name='setup_rates'),
    path('input_previous_usage/', views.input_previous_usage, name='input_previous_usage'),
    path('calculate_bill/', views.calculate_bill, name='calculate_bill'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),

]
