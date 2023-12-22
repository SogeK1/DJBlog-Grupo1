from django.db import models
from django.utils import timezone

# Create your models here.

'''
Aquí se define una clase llamada Contacto, 
que hereda de la clase Model de Django. 
Esta clase representa un modelo de base de datos.
'''
class Contacto(models.Model):
    
    '''
    Este campo representa el nombre completo del 
    contacto y está definido como un campo de caracteres 
    (CharField) con una longitud máxima de 120 caracteres.
    '''
    nombre_completo = models.CharField(max_length=120)
    
    '''
    Este campo representa la dirección de correo electrónico 
    del contacto y está definido como un campo de correo electrónico (EmailField).
    '''
    email = models.EmailField()
    
    '''
    Este campo representa el asunto del mensaje y está definido como un campo de 
    caracteres (CharField) con una longitud máxima de 50 caracteres.
    '''
    asunto = models.CharField(max_length=50)
    
    '''
    Este campo representa el cuerpo del mensaje y está definido como un campo de 
    texto (TextField), lo que significa que puede contener una cantidad significativa de texto.
    '''
    mensaje = models.TextField()
    
    '''
    Este campo representa la fecha y hora en que se creó el registro. Se utiliza un campo de 
    fecha y hora (DateTimeField), y se establece el valor predeterminado en el momento actual 
    utilizando timezone.now.
    '''
    fecha = models.DateTimeField(default=timezone.now)
    
    '''
    Este método __str__ define cómo se debe representar el objeto Contacto como una cadena. 
    En este caso, se devuelve el nombre completo del contacto como representación de cadena.
    '''
    def __str__(self):
        return self.nombre_completo
