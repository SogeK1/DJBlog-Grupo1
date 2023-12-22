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
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Iniciaste sesión')

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
        # return reverse('index')
        
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context
    
    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(usuario=self.object).delete()

        if eliminar_posts:
            Post.objects.filet(autor=self.object)
            messages.success(request,f'usuario {self.object.username} eliminado correctamente')
            return self.delete(request, *args, **kwargs)
        