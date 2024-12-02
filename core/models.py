from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Extendemos el modelo de usuario predeterminado
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return self.username

class TransferReason(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.ForeignKey(TransferReason, on_delete=models.PROTECT, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorited_by')
