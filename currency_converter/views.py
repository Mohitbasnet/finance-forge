from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import requests
import json
from decimal import Decimal
from .models import UserProfile, CurrencyTransaction, SavedQuote, InvestmentQuote
from .forms import UserProfileForm, UserUpdateForm, CustomUserCreationForm

def home(request):
    """Home page view"""
    return render(request, 'currency_converter/home.html')

def register(request):
    """Enhanced user registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to Finance Forge, {user.first_name}!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'currency_converter/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'currency_converter/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            # Check if user exists to provide more specific error
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'Username not found. Please check your username or create a new account.')
    return render(request, 'currency_converter/login.html')

@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard view"""
    user_transactions = CurrencyTransaction.objects.filter(user=request.user).order_by('-transaction_date')[:5]
    saved_quotes = SavedQuote.objects.filter(user=request.user).order_by('-quote_date')[:5]
    investment_quotes = InvestmentQuote.objects.filter(user=request.user).order_by('-quote_date')[:5]
    
    context = {
        'transactions': user_transactions,
        'saved_quotes': saved_quotes,
        'investment_quotes': investment_quotes,
    }
    return render(request, 'currency_converter/dashboard.html', context)

def currency_converter(request):
    """Currency converter view"""
    currencies = {
        'GBP': 'British Pound Sterling',
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'BRL': 'Brazilian Real',
        'JPY': 'Japanese Yen',
        'TRY': 'Turkish Lira'
    }
    
    context = {
        'currencies': currencies,
    }
    return render(request, 'currency_converter/currency_converter.html', context)

@csrf_exempt
def convert_currency(request):
    """API endpoint for currency conversion"""
    print(f"Request method: {request.method}")
    print(f"Request body: {request.body}")
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Parsed data: {data}")
            from_currency = data.get('from_currency')
            to_currency = data.get('to_currency')
            amount = Decimal(data.get('amount', 0))
            print(f"From: {from_currency}, To: {to_currency}, Amount: {amount}")
            
            # Using a free currency API (you might want to use a paid service for production)
            # For demo purposes, we'll use a simple conversion rate
            # In production, you should use a real-time currency API
            
            # Mock exchange rates (in production, fetch from API)
            exchange_rates = {
                'GBP': {'USD': 1.25, 'EUR': 1.15, 'BRL': 6.20, 'JPY': 180.0, 'TRY': 38.0, 'GBP': 1.0},
                'USD': {'GBP': 0.80, 'EUR': 0.92, 'BRL': 4.96, 'JPY': 144.0, 'TRY': 30.4, 'USD': 1.0},
                'EUR': {'GBP': 0.87, 'USD': 1.09, 'BRL': 5.39, 'JPY': 156.5, 'TRY': 33.0, 'EUR': 1.0},
                'BRL': {'GBP': 0.16, 'USD': 0.20, 'EUR': 0.19, 'JPY': 29.0, 'TRY': 6.13, 'BRL': 1.0},
                'JPY': {'GBP': 0.0056, 'USD': 0.0069, 'EUR': 0.0064, 'BRL': 0.034, 'TRY': 0.21, 'JPY': 1.0},
                'TRY': {'GBP': 0.026, 'USD': 0.033, 'EUR': 0.030, 'BRL': 0.163, 'JPY': 4.74, 'TRY': 1.0},
            }
            
            print(f"Checking currencies: {from_currency} in rates: {from_currency in exchange_rates}")
            print(f"Available rates for {from_currency}: {list(exchange_rates.get(from_currency, {}).keys())}")
            
            if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
                rate = Decimal(str(exchange_rates[from_currency][to_currency]))
                converted_amount = amount * rate
                print(f"Rate: {rate}, Converted amount: {converted_amount}")
                
                # Save transaction if user is logged in
                if request.user.is_authenticated:
                    CurrencyTransaction.objects.create(
                        user=request.user,
                        from_currency=from_currency,
                        to_currency=to_currency,
                        amount=amount,
                        converted_amount=converted_amount,
                        exchange_rate=rate,
                        transaction_type='BUY'
                    )
                
                return JsonResponse({
                    'success': True,
                    'converted_amount': float(converted_amount),
                    'exchange_rate': float(rate),
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'amount': float(amount)
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid currency pair'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def save_quote(request):
    """Save a currency conversion quote"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            SavedQuote.objects.create(
                user=request.user,
                from_currency=data['from_currency'],
                to_currency=data['to_currency'],
                amount=Decimal(data['amount']),
                converted_amount=Decimal(data['converted_amount']),
                exchange_rate=Decimal(data['exchange_rate']),
                notes=data.get('notes', '')
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def investment_calculator(request):
    """Investment calculator view"""
    return render(request, 'currency_converter/investment_calculator.html')

@login_required
@csrf_exempt
def calculate_investment(request):
    """Calculate investment returns"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            initial_amount = Decimal(data['initial_amount'])
            return_rate = Decimal(data['return_rate'])
            time_period = int(data['time_period'])
            investment_type = data['investment_type']
            
            # Calculate compound interest
            final_amount = initial_amount * (1 + return_rate / 100) ** time_period
            
            # Save investment quote
            InvestmentQuote.objects.create(
                user=request.user,
                investment_type=investment_type,
                initial_amount=initial_amount,
                expected_return_rate=return_rate,
                time_period_years=time_period,
                expected_final_amount=final_amount,
                notes=data.get('notes', '')
            )
            
            return JsonResponse({
                'success': True,
                'final_amount': float(final_amount),
                'total_return': float(final_amount - initial_amount)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def transaction_history(request):
    """View transaction history"""
    transactions = CurrencyTransaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'currency_converter/transaction_history.html', {'transactions': transactions})

@login_required
def saved_quotes(request):
    """View saved quotes"""
    quotes = SavedQuote.objects.filter(user=request.user).order_by('-quote_date')
    return render(request, 'currency_converter/saved_quotes.html', {'quotes': quotes})

@login_required
def investment_history(request):
    """View investment quotes history"""
    investments = InvestmentQuote.objects.filter(user=request.user).order_by('-quote_date')
    return render(request, 'currency_converter/investment_history.html', {'investments': investments})

@login_required
def profile(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    # Get user statistics
    total_transactions = CurrencyTransaction.objects.filter(user=request.user).count()
    total_saved_quotes = SavedQuote.objects.filter(user=request.user).count()
    total_investments = InvestmentQuote.objects.filter(user=request.user).count()
    
    # Get recent activity
    recent_transactions = CurrencyTransaction.objects.filter(user=request.user).order_by('-transaction_date')[:5]
    recent_quotes = SavedQuote.objects.filter(user=request.user).order_by('-quote_date')[:5]
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
        'total_transactions': total_transactions,
        'total_saved_quotes': total_saved_quotes,
        'total_investments': total_investments,
        'recent_transactions': recent_transactions,
        'recent_quotes': recent_quotes,
    }
    
    return render(request, 'currency_converter/profile.html', context)

@login_required
def change_password(request):
    """Change password view"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please log in again.')
            return redirect('login')
    
    return render(request, 'currency_converter/change_password.html')
