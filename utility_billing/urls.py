# utility_billing/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import billing.views
from billing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls', namespace='billing')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('', billing.views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('captcha/', include('captcha.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
