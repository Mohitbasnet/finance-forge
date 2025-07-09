from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    CURRENCY_PREFERENCE_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('BRL', 'Brazilian Real'),
        ('TRY', 'Turkish Lira'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_PREFERENCE_CHOICES, default='USD')
    notification_preferences = models.JSONField(default=dict, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class CurrencyTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.from_currency} to {self.converted_amount} {self.to_currency}"

class SavedQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6)
    quote_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Quote for {self.amount} {self.from_currency}"

class InvestmentQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=50)
    initial_amount = models.DecimalField(max_digits=15, decimal_places=2)
    expected_return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    time_period_years = models.IntegerField()
    expected_final_amount = models.DecimalField(max_digits=15, decimal_places=2)
    quote_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.investment_type} Investment Quote"
