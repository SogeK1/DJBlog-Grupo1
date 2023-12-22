from django import forms
from .models import Contacto

# Define una nueva clase llamada ContactoForm que hereda de forms.ModelForm 
# se utiliza para crear formularios basados en modelos
class ContactoForm(forms.ModelForm):
    # Esta clase Meta se utiliza para proporcionar metadatos adicionales al formulario
    class Meta:
        # Especifica el modelo asociado con este formulario, que es el modelo Contacto 
        # Esto significa que el formulario se construirá para manejar datos que se alineen con el modelo
        model = Contacto
        # Estos son los campos que el usuario deberá completar cuando utilice este formulario
        fields = ['nombre_completo', 'email', 'asunto', 'mensaje']
        