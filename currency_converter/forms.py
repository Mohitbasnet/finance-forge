from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 
            'address', 
            'date_of_birth', 
            'gender', 
            'profile_picture', 
            'bio', 
            'website', 
            'preferred_currency'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your address...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+1 (555) 123-4567'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
        }

class UserUpdateForm(forms.ModelForm):
    """Form for updating basic user information"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }

class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True 