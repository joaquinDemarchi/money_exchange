from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import User, Transaction, TransferReason
from .forms import UserRegistrationForm, ProfileUpdateForm, TransactionForm, UserUpdateForm, TransactionReasonForm, DepositForm

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


# adminsitrar perfil
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
    
class UserProfileView(TemplateView):
    template_name = 'core/profile.html'


# Administración usuario
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


# Administrar razones 
class AdminReasonListView(ListView):
    model = TransferReason
    template_name = 'core/admi_reasons.html'
    context_object_name = 'reasons'

class AdminReasonDeleteView(DeleteView):
    model = TransferReason
    template_name = 'core/reason_delete.html' 
    form_class = TransactionReasonForm 
    context_object_name = 'reasons'
    
    def post(self, request, *args, **kwargs):
            # Añadir debug aquí para asegurar que el objeto se elimina
            obj = self.get_object()
            print(f"Eliminando objeto: {obj}")  # Verifica el objeto que se va a eliminar
            response = super().post(request, *args, **kwargs)  # Llamada a la eliminación
            print("Eliminación completada")
            
            return HttpResponseRedirect(reverse_lazy('admi_reasons'))

class AdminReasonUpdateView(UpdateView):
    model = TransferReason
    template_name = 'core/reason_edit.html'
    form_class = TransactionReasonForm
    context_object_name = 'reasons'
    success_url = reverse_lazy('admi_reasons')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Actulizar Motivo"
        return ctx


# Transferencias
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'core/transaction_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        
        form.instance.sender = self.request.user # asigno como enviador al usr de la sesion
        
        if self.request.user.balance < form.instance.amount: #comporbacion si el saldo es menor al monto de la tx
            form.add_error('amount', 'Saldo insuficiente.')
            return self.form_invalid(form)
        form.instance.sender.balance -= form.instance.amount # actulizo saldo del enviador
        form.instance.recipient.balance += form.instance.amount # actulizo saldo del receptor
        
        #guardo cambios
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
    

class UserTransactionDetailView(DetailView):
    model = User
    template_name = 'core/user_transactions_detail.html'  # La plantilla que vamos a crear
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object  # El usuario que se está viendo
        
        # Obtengo tx salientes del usr  como emisor
        sent_transactions = Transaction.objects.filter(sender=user)
        
        # Obtengo tx entrantes del usr como receptor
        received_transactions = Transaction.objects.filter(recipient=user)
        
        # Añadir estas transacciones al contexto
        context['sent_transactions'] = sent_transactions
        context['received_transactions'] = received_transactions
        
        return context
    
# Vista para el depósito de dinero
class DepositView(View):
    template_name = 'core/deposit_form.html'

    # GET: Muestra el formulario
    def get(self, request):
        form = DepositForm()  # Creamos el formulario vacío
        return render(request, self.template_name, {'form': form})

    # POST: Procesa el depósito
    def post(self, request):
        form = DepositForm(request.POST)  # Recibe los datos del formulario
        if form.is_valid():
            amount = form.cleaned_data['amount']  # Obtiene el monto ingresado
            user = request.user  # El usuario actual

            # Verificamos si el monto es positivo
            if amount <= 0:
                form.add_error('amount', 'El monto debe ser mayor que cero.')
                return render(request, self.template_name, {'form': form})

            # Realizamos la transacción (agregar saldo al usuario)
            user.balance += amount
            user.save()

            # Buscamos o creamos el motivo "Depósito de dinero"
            reason, created = TransferReason.objects.get_or_create(name="Depósito de dinero")

            # Creamos el registro de la transacción
            transaction = Transaction.objects.create(
                sender=user,  # El usuario es tanto el remitente como el receptor
                recipient=user,
                amount=amount,
                reason=reason,  # Asignamos la instancia de TransferReason
            )

            # Enviamos un mensaje de éxito
            messages.success(request, f'Has depositado ${amount} exitosamente a tu cuenta.')
            return redirect('profile')  # Redirige al perfil del usuario

        # Si el formulario no es válido, lo volvemos a mostrar con los errores
        return render(request, self.template_name, {'form': form})