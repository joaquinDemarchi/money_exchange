from django.contrib import admin

from .models import User, Favorite, Transaction, TransferReason

#para registrar usuarios desde el admin
#la contra no se encripta
admin.site.register(User)

#para registrar favoritos desde el admin
admin.site.register(Favorite)

#para registrar motivos de transferencia desde el admin
admin.site.register(TransferReason)


