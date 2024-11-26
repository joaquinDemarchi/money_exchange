from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import HomeView, UserRegistrationView, UserLoginView, UserProfileView, TransactionCreateView, AdminUserListView, AdminReasonListView, UserLogoutView, ProfileUpdateView, TransactionDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='pf_update'),
    path('transfer/', TransactionCreateView.as_view(), name='transfer'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/reasons/', AdminReasonListView.as_view(), name='admin_reasons'),
]