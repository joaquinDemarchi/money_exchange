from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import User, Transaction, TransferReason
from .forms import UserRegistrationForm, ProfileUpdateForm, TransactionForm

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

# Perfil del usuario
class UserProfileView(TemplateView):
    template_name = 'core/profile.html'

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

# Administración
class AdminUserListView(ListView):
    model = User
    template_name = 'core/admin_users.html'
    context_object_name = 'users'

class AdminReasonListView(ListView):
    model = TransferReason
    template_name = 'core/admin_reasons.html'
    context_object_name = 'reasons'
    
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige a la página de login después de cerrar sesión

class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'core/profile_update.html'
    success_url = reverse_lazy('profile')  # Redirige a la vista de perfil después de la actualización
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Actuliza el perfil del usuario"
        return ctx

    # Método para asegurarse de que solo el usuario logueado pueda editar su propio perfil
    def get_object(self, queryset=None):
        return self.request.user
    
class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'core/transaction_detail.html'
    context_object_name = 'transaction'