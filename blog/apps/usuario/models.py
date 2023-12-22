from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

'''
Define una nueva clase llamada Usuario 
que hereda de AbstractUser. 
AbstractUser es una clase proporcionada 
por Django que contiene la implementación 
básica de un modelo de usuario. 
Al heredar de esta clase, 
estás extendiendo la funcionalidad 
básica del modelo de usuario.
'''
class Usuario(AbstractUser):
    '''
    Agrega un campo de imagen llamado imagen al modelo Usuario. 
    Este campo utiliza models.ImageField para almacenar imágenes. 
    Los parámetros utilizados son: 
    null=True: Permite que el campo almacene valores nulos en la base de datos.
    blank=True: Permite que el campo sea opcional en formularios.
    upload_to='usuario': Especifica la subcarpeta dentro del directorio de medios donde se almacenarán las imágenes.
    default='usuario/user-default.png': Proporciona una imagen predeterminada si no se proporciona ninguna imagen.
    '''
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario', default='usuario/user-default.png')
    
    '''
    Define un método llamado get_absolute_url. 
    Este método se utiliza para proporcionar la URL absoluta del objeto Usuario. 
    En este caso, siempre redirige a la página con el nombre de ruta 'index'. 
    Esto es útil en ciertos contextos, 
    como al utilizar la función get_absolute_url en las vistas genéricas de Django.
    '''
    
    def get_absolute_url(self):
        return reverse('index')