from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Transaction, TransferReason

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['recipient', 'amount', 'reason']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name','is_admin',  'email']
        