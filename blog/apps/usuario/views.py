from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib import messages
from .models import Usuario
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from apps.posts.models import Comentario, Post

# Create your views here.

'''
RegistrarUsuario hereda de CreateView, que es una vista de 
Django para crear instancias de modelos en la base de datos.
'''
class RegistrarUsuario(CreateView):
    '''
    template_name especifica la plantilla HTML que se utilizará 
    para renderizar la vista de registro.
    '''
    template_name = 'registration/registrar.html'
    '''
    forms_class especifica la clase de formulario a utilizar, 
    en este caso, RegistroUsuarioForm.
    '''
    form_class = RegistroUsuarioForm
    
    
    '''
    El método form_valid se llama cuando el formulario es válido. 
    Aquí se guarda el formulario, se muestra un mensaje de éxito y 
    luego se redirige al usuario a la URL especificada ('apps.usuario:registrar').
    '''
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro exitoso. Porfavor, inicia sesión.')
        group = Group.objects.get(name='Registrado')
        self.object.groups.add(group)
        return redirect('apps.usuario:registrar')
        # form.save()
    

    
'''
loginUsuario hereda de LoginView, que es una vista de Django para manejar el inicio de sesión de usuarios.
'''
class LoginUsuario(LoginView):
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista. En este caso, la plantilla se 
    encuentra en 'registration/login.html'.
    '''
    template_name = 'registration/login.html'

    '''
    Se define el método get_success_url, que se encarga de proporcionar la URL a la que se redirigirá después 
    de que el usuario haya iniciado sesión correctamente.
    '''
    def get_success_url(self):
        
        '''
        Se utiliza messages.success para enviar un mensaje de éxito que se mostrará en la interfaz del usuario después de iniciar sesión.
        '''
        messages.success(self.request, 'Iniciaste sesión')

        '''
        Se utiliza reverse_lazy para obtener la URL a la que se redirigirá después del inicio de sesión exitoso. En este caso, se redirige 
        a la URL con nombre 'index'. Asegúrate de tener una URL con este nombre definida en tu archivo de configuración de URL (por lo general, en urls.py), o ajusta este valor según la estructura de tus URLs.
        '''
        return reverse_lazy('index')


'''
LogoutUsuario hereda de LogoutView, que es una vista de Django para manejar el cierre de sesión de usuarios.

'''
class LogoutUsuario(LogoutView):
    '''
    template_name especifica la plantilla HTML que se utilizará para renderizar la vista de cierre de sesión.
    '''
    template_name = 'registration/logout.html'
    
    '''
    get_success_url es un método que se llama después de que el usuario cierra sesión con éxito. 
    Muestra un mensaje de éxito y redirige al usuario a la URL especificada ('apps.usuario:logout').
    '''
    def get_success_url(self):
        messages.success(self.request, 'Cerraste sesión')
        
        return reverse('apps.usuario:logout')

'''
Se define la clase UsuarioListView, que hereda tanto de LoginRequiredMixin como de ListView. 
Esto indica que esta vista requiere que el usuario esté autenticado para acceder y se utilizará 
para mostrar una lista de objetos del modelo Usuario.
'''
class UsuarioListView(LoginRequiredMixin, ListView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se mostrarán. En este caso, es el modelo Usuario.
    '''
    model = Usuario
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista. Asegúrate de tener la plantilla adecuada 
    en la ubicación correcta.
    '''
    template_name = 'usuarios/usuario_list.html'
    
    '''
    Especifica el nombre del contexto que se utilizará en la plantilla para referenciar la lista de objetos Usuario. 
    En la plantilla, se puede acceder a esta lista utilizando el nombre 'usuarios'.
    '''
    context_object_name = 'usuarios'
    
    '''
    El método get_queryset se sobrescribe para modificar la consulta que obtiene la lista de usuarios.
    '''
    def get_queryset(self):
        
        '''
        super().get_queryset() llama al método de la clase base para obtener la consulta original.
        '''
        queryset = super().get_queryset()
        
        '''
        En este caso, se utiliza exclude(is_superuser=True) para excluir a los usuarios con el atributo is_superuser 
        establecido en True, es decir, los superusuarios. Esto significa que la lista de usuarios que se mostrará en 
        la vista no incluirá a los superusuarios.
        '''
        queryset = queryset.exclude(is_superuser=True)
        return queryset

'''
Se define la clase UsuarioDeleteView que hereda de LoginRequiredMixin y DeleteView. Esta vista se utiliza para eliminar
un objeto Usuario. Se especifica la plantilla que se utilizará ('usuarios/eliminar_usuario.html') y la URL a la que se 
redirigirá después de la eliminación exitosa.
'''
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    
    
    model = Usuario
    template_name = 'usuarios/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    '''
    El método get_context_data se sobrescribe para agregar datos adicionales al contexto que se pasará a la plantilla. 
    En este caso, se comprueba si el usuario es miembro del grupo 'Colaborador' y se agrega esta información al contexto.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context
    
    '''
    El método post maneja la lógica de la solicitud POST, que ocurre cuando el usuario confirma la eliminación del objeto 
    Usuario. Se obtienen las opciones (eliminar_comentarios y eliminar_posts) de la solicitud POST y se realiza la acción 
    correspondiente:
    Si eliminar_comentarios es True, se eliminan todos los comentarios asociados al usuario.
    Si eliminar_posts es True, se eliminan todos los posts asociados al usuario, y se muestra un mensaje de éxito.
    '''
    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(usuario=self.object).delete()

        if eliminar_posts:
            Post.objects.filter(autor=self.object)
            messages.success(request,f'usuario {self.object.username} eliminado correctamente')
            return self.delete(request, *args, **kwargs)
        