from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import HomeView, UserRegistrationView, UserLoginView, UserProfileView, TransactionCreateView, AdminUserListView, AdminReasonListView, UserLogoutView, ProfileUpdateView, TransactionDetailView, TransactionList, AdminUserUpdateView, AdminUserDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='pf_update'),
    path('transfer/', TransactionCreateView.as_view(), name='transfer'),
    path('transferlist/', TransactionList.as_view(), name='transfer_list'),
    path('transferlist/details/<int:pk>/', TransactionDetailView.as_view(), name='transfer_details'),
    path('admi/users/', AdminUserListView.as_view(), name='admi_users'),
    path('admi/users/edit/<int:pk>/', AdminUserUpdateView.as_view(), name='edit_users'),
    path('admi/users/delete/<int:pk>/', AdminUserDeleteView.as_view(), name='delete_user'), 
    path('admi/reasons/', AdminReasonListView.as_view(), name='admi_reasons'),
]