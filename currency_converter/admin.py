from django.contrib import admin
from .models import UserProfile, CurrencyTransaction, SavedQuote, InvestmentQuote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CurrencyTransaction)
class CurrencyTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_currency', 'to_currency', 'amount', 'converted_amount', 'transaction_type', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date', 'from_currency', 'to_currency')
    search_fields = ('user__username', 'from_currency', 'to_currency')
    readonly_fields = ('transaction_date',)
    date_hierarchy = 'transaction_date'

@admin.register(SavedQuote)
class SavedQuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_currency', 'to_currency', 'amount', 'converted_amount', 'exchange_rate', 'quote_date')
    list_filter = ('quote_date', 'from_currency', 'to_currency')
    search_fields = ('user__username', 'from_currency', 'to_currency', 'notes')
    readonly_fields = ('quote_date',)
    date_hierarchy = 'quote_date'

@admin.register(InvestmentQuote)
class InvestmentQuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_type', 'initial_amount', 'expected_return_rate', 'time_period_years', 'expected_final_amount', 'quote_date')
    list_filter = ('investment_type', 'quote_date', 'expected_return_rate')
    search_fields = ('user__username', 'investment_type', 'notes')
    readonly_fields = ('quote_date', 'expected_final_amount')
    date_hierarchy = 'quote_date'
