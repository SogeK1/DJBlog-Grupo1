from django.contrib import admin
from .models import Contacto

# Register your models here.

@admin.register(Contacto) #registro de clase

# declaramos una clase Para luego poder 
# usar un "list_display" con los atributos 
# que queramos mostrar
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('mensaje', 'nombre_completo', 'email', 'asunto', 'fecha',)