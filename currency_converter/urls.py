from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('converter/', views.currency_converter, name='currency_converter'),
    path('convert/', views.convert_currency, name='convert_currency'),
    path('save-quote/', views.save_quote, name='save_quote'),
    path('investment-calculator/', views.investment_calculator, name='investment_calculator'),
    path('calculate-investment/', views.calculate_investment, name='calculate_investment'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('saved-quotes/', views.saved_quotes, name='saved_quotes'),
    path('investment-history/', views.investment_history, name='investment_history'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
] 