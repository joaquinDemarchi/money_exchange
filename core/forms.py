from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User, Transaction, TransferReason

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','balance', 'is_admin','is_active_account' ]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['recipient', 'amount', 'reason']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name',  'email']
        

class TransactionReasonForm(forms.ModelForm):
    class Meta:
        model = TransferReason
        fields = ['id', 'name']
        

#ingresar dinero
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Monto a depositar")

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return amount