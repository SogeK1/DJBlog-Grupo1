from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.

'''
Registra el modelo Usuario para que sea administrado a través del panel de administración 
de Django. Además, se utiliza la clase UserAdmin para personalizar la forma en que se 
presenta y administra el modelo de usuario en el panel de administración.
'''
admin.site.register(Usuario, UserAdmin)