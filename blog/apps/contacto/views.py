from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

'''
es una vista basada en clase 
que se utiliza para manejar 
la creación de instancias de 
modelos en una base de datos. 
En este caso, se utiliza para 
manejar la creación de instancias de
un formulario llamado ContactoForm.
'''
class ContactoUsuario(CreateView):
    # Especifica la plantilla HTML que se utilizará para renderizar la vista
    template_name = 'contacto/contacto.html'
    # Define la clase del formulario que se utilizará en esta vista
    form_class = ContactoForm
    '''
    Indica a dónde se redirigirá al usuario después de 
    que el formulario se haya enviado correctamente
    el usuario será redirigido a la URL inversa ('index')
    '''
    success_url = reverse_lazy('index')
    '''
     Este método se llama cuando el formulario es válido y 
     se está listo para ser procesado. En este caso, 
     se sobrescribe el método para agregar una notificación de 
     éxito (messages.success) que se mostrará al usuario. Luego, 
     se llama al método super().form_valid(form) para realizar la 
     lógica predeterminada de procesamiento del formulario.
    '''
    def form_valid(self, form):
        messages.success(self.request, 'Consulta enviada.')
        return super().form_valid(form)
