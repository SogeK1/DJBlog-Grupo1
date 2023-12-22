from django.urls import path
from . import views

'''
La variable app_name se utiliza para definir un espacio de nombres para las URL de la aplicación. 
En este caso, se establece en 'apps.contacto', lo que significa que las URLs de esta aplicación 
deben tener un prefijo que coincida con este espacio de nombres.
'''
app_name = 'apps.contacto'

'''
este código configura una única URL para la aplicación con el nombre 'contacto', 
que se activará cuando la ruta sea 'contacto/'. La vista asociada es ContactoUsuario 
definida en el archivo views de la aplicación.
'''
urlpatterns = [
    path('contacto/', views.ContactoUsuario.as_view(), name='contacto'),
]

