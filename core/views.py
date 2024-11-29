from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import User, Transaction, TransferReason
from .forms import UserRegistrationForm, ProfileUpdateForm, TransactionForm, UserUpdateForm

# Inicio y registro
class HomeView(TemplateView):
    template_name = 'core/home.html'

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'core/login.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(UserLoginView, self).get_context_data(**kwargs)
        ctx["titulo"] = "Bienvenido a la plataforma"
        return ctx

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  

# Perfil del usuario
class UserProfileView(TemplateView):
    template_name = 'core/profile.html'


# Administración
class AdminUserListView(ListView):
    model = User
    template_name = 'core/admi_users.html'
    context_object_name = 'users'

class AdminUserUpdateView(UpdateView):
    model = User
    template_name = 'core/edit_users.html'
    form_class = UserUpdateForm
    context_object_name = 'users'
    success_url = reverse_lazy('admi_users')
    #fields = ['username', 'first_name', 'last_name']

class AdminUserDeleteView(DeleteView):
    model = User
    template_name = 'core/delete_user.html'  
    context_object_name = 'user'
    success_url = reverse_lazy('admi_users')  

class AdminReasonListView(ListView):
    model = TransferReason
    template_name = 'core/admi_reasons.html'
    context_object_name = 'reasons'

class AdminReasonDeleteView(DeleteView):
    model = TransferReason
    template_name = 'core/reason_delete.html'  
    context_object_name = 'reasons'
    success_url = reverse_lazy('admi_reasons')

class AdminReasonUpdateView(UpdateView):
    model = TransferReason
    template_name = 'core/reason_edit.html'
    form_class = TransferReason
    context_object_name = 'reasons'
    success_url = reverse_lazy('admi_reasons')

class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'core/profile_update.html'
    success_url = reverse_lazy('profile')  
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Actuliza el perfil del usuario"
        return ctx

    # Método para asegurarse de que solo el usuario logueado pueda editar su propio perfil
    def get_object(self, queryset=None):
        return self.request.user

# Transferencias
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'core/transaction_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        
        form.instance.sender = self.request.user
        
        if self.request.user.balance < form.instance.amount:
            form.add_error('amount', 'Saldo insuficiente.')
            return self.form_invalid(form)
        form.instance.sender.balance -= form.instance.amount
        form.instance.recipient.balance += form.instance.amount
        form.instance.sender.save()
        form.instance.recipient.save()
        
        return super().form_valid(form)
class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'core/transaction_detail.html'
    context_object_name = 'transaction'
    
class TransactionList(ListView):
    model = Transaction
    template_name = 'core/transaction_list.html'
    context_object_name = 'transactions'