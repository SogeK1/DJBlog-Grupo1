from django.shortcuts import render, redirect
from .models import Post, Comentario, Categoria
from .forms import ComentarioForm, CrearPostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from .models import Post

# Create your views here.

'''
Se define la clase PostListView que hereda de ListView. Esto indica que PostListView es 
una vista basada en clase que utiliza la funcionalidad proporcionada por ListView para 
mostrar una lista de objetos Post.
'''
class PostListView(ListView):
    
    '''
    Se especifica el modelo cuyos objetos se mostrarán en la lista. En este caso, son objetos del modelo Post.
    '''
    model = Post
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista. En este caso, 
    la plantilla se encuentra en 'posts/posts.html'.
    '''
    template_name = 'posts/posts.html'
    
    '''
    Especifica el nombre del contexto que se utilizará en la plantilla para referenciar la lista de objetos Post. 
    En la plantilla, se puede acceder a esta lista utilizando el nombre 'posts'.
    '''
    context_object_name = 'posts'

    '''
    El método get_queryset se sobrescribe para proporcionar la lógica de obtener y ordenar la lista de objetos Post. 
    Dependiendo del valor del parámetro 'orden' en la URL, se realiza una ordenación específica 
    (por fecha en orden ascendente o descendente, o alfabéticamente por título).
    '''
    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden', 'reciente')  # Valor predeterminado: 'reciente'
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset

    
    '''
    El método get_context_data se sobrescribe para proporcionar datos adicionales al contexto de la plantilla. 
    En este caso, se añade la variable 'orden' al contexto, que contiene el valor del parámetro 'orden' en la 
    URL o el valor predeterminado 'reciente'.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context

    
# Vista basada en clase que se utiliza para mostrar una publicación específica
class PostDetailView(DetailView):
    # Modelo que representa los datos de la publicación
    model = Post
    # Template que se utilizará para renderizar la publicacion
    template_name = 'posts/post_individual.html' 
    # Nombre del contexto que se utilizará para pasar la publicacion al template
    context_object_name = 'posts'
    # Nombre del parámetro de la URL que se utiliza para identificar la publicación específica
    pk_url_kwarg = 'id'
    # Define el conjunto de publicaciones del que se seleccionará la específica
    queryset = Post.objects.all()
    
    '''
    Es parte de la clase PostDetailView y se utiliza para 
    agregar datos adicionales al contexto que se pasa a la plantilla. 
    '''
    def get_context_data(self, **kwargs):
        
        '''
        Llama al método get_context_data de la clase principal (super()) 
        para obtener el contexto que se generaría normalmente. 
        Esto es útil para asegurarse de que cualquier contexto que la 
        clase principal quiera pasar se incluya en nuestro contexto personalizado.
        '''
        context = super().get_context_data(**kwargs)
        
        '''
        Agrega un formulario de comentario (ComentarioForm) al contexto. Esto significa 
        que en la plantilla asociada a esta vista, se puede acceder al formulario usando la 
        variable de contexto form.
        '''
        context['form'] = ComentarioForm()
        
        '''
        Comentario.objects.filter(posts_id=self.kwargs['id']): Agrega los 
        comentarios asociados a la publicación actual al contexto. 
        Utiliza el modelo Comentario y el método filter para obtener todos los 
        comentarios cuyo campo posts_id coincide con el identificador de la 
        publicación actual (self.kwargs['id']). Estos comentarios se pueden acceder 
        en la plantilla usando la variable de contexto comentarios.
        '''
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        
        '''
        Devuelve el contexto modificado que incluye el formulario y los comentarios adicionados.
        '''
        return context 
    
    '''
    Este método post es parte de la clase PostDetailView y se encarga de manejar las solicitudes HTTP POST, 
    particularmente cuando se envía el formulario para agregar un comentario a una publicación. 
    '''
    def post(self, request, *args, **kwargs):
        
        '''
        Crea una instancia del formulario ComentarioForm utilizando los datos del formulario POST enviado 
        por el usuario.
        '''
        form = ComentarioForm(request.POST)
        
        '''
        Verifica si el formulario es válido, es decir, si pasa las validaciones definidas en la clase 
        ComentarioForm.
        '''
        if form.is_valid():
            
            '''
            Crea una instancia de la clase Comentario utilizando los datos del formulario, 
            pero no la guarda en la base de datos todavía. El parámetro commit=False evita la 
            persistencia inmediata en la base de datos.
            '''
            comentario = form.save(commit=False)
            
            '''
            Asigna al campo usuario de la instancia de comentario el usuario actual que realizó la solicitud.
            '''
            comentario.usuario = request.user
            
            '''
            Asigna al campo posts_id de la instancia de comentario el identificador de la publicación actual, 
            que se obtiene de los parámetros de la URL (self.kwargs['id']).
            '''
            comentario.posts_id = self.kwargs['id']
            
            '''
            Guarda finalmente la instancia del comentario en la base de datos.
            '''
            comentario.save()
            
            '''
            Redirige al usuario a la vista de detalle de la publicación (post_individual) 
            después de agregar el comentario. Se incluye el identificador de la 
            publicación en la redirección.
            '''
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        
        else:
            
            '''
            Se obtiene el contexto actual utilizando el método get_context_data. 
            Este método agrega el formulario de comentarios (ComentarioForm) 
            y los comentarios asociados a la publicación actual al contexto.
            '''
            context = self.get_context_data(**kwargs)
            '''
            Se agrega el formulario no válido al contexto. Esto asegura que el 
            formulario no válido esté disponible en el contexto de la plantilla 
            para que pueda ser mostrado junto con los mensajes de error.
            '''
            context['form'] = form
            
            '''
            Se renderiza la respuesta utilizando el contexto actualizado que 
            incluye el formulario no válido y otros datos necesarios. 
            Esto implica que la vista de detalle de la publicación será 
            renderizada nuevamente, pero ahora con el formulario y 
            los mensajes de error visibles.
            '''
            return self.render_to_response(context)
        
    '''
    Define una nueva clase llamada ComentarioCreateView 
    que hereda de LoginRequiredMixin y CreateView. 
    Esto significa que esta vista requerirá que el usuario 
    esté autenticado y se utilizará para la creación de 
    nuevos comentarios.
    '''

'''
Se define la clase PostCreateView, que hereda tanto de LoginRequiredMixin como de CreateView. 
Esto indica que esta vista requiere autenticación para acceder y que se utilizará para la 
creación de objetos del modelo Post.
'''
class PostCreateView(LoginRequiredMixin,CreateView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se crearán. 
    En este caso, es el modelo Post.
    '''
    model = Post
    
    '''
    Se especifica la clase del formulario que se utilizará para recoger la información del usuario.
    En este caso, es la clase CrearPostForm.
    '''
    form_class = CrearPostForm
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista. En este caso, es 
    'posts/crear_post.html'.
    '''
    template_name = 'posts/crear_post.html'
    
    '''
    Se especifica la URL a la que se redirigirá después de que se haya creado con éxito un nuevo objeto Post. 
    reverse_lazy se utiliza para invertir la URL basada en el nombre, en este caso, la URL llamada 'apps.posts:posts'.
    '''
    success_url = reverse_lazy('apps.posts:posts')

'''
Se define la clase PostUpdateView, que hereda tanto de LoginRequiredMixin como de UpdateView. Esto indica que esta vista 
requiere autenticación para acceder y que se utilizará para la actualización de objetos del modelo Post.
'''
class PostUpdateView(LoginRequiredMixin,UpdateView):
    
    '''
     Se especifica el modelo al que pertenecen los objetos que se actualizarán. En este caso, es el modelo Post.
    '''
    model = Post
    
    '''
    Se especifica la clase del formulario que se utilizará para recoger la información del usuario. En este caso, 
    es la clase CrearPostForm.
    '''
    form_class = CrearPostForm
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista de actualización. En este caso, 
    es 'posts/modificar_post.html'.
    '''
    template_name = 'posts/modificar_post.html'
    
    '''
    Se especifica la URL a la que se redirigirá después de que se haya actualizado con éxito un objeto Post. 
    reverse_lazy se utiliza para invertir la URL basada en el nombre, en este caso, la URL llamada 'apps.posts:posts'.
    '''
    success_url =  reverse_lazy('apps.posts:posts')
   
'''
Se define la clase PostDeleteView, que hereda de DeleteView. Esto indica que esta vista se utilizará para la eliminación 
de objetos del modelo Post.
'''
class PostDeleteView(DeleteView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se eliminarán. En este caso, es el modelo Post.
    '''
    model = Post
    
    '''
     Se especifica la plantilla que se utilizará para renderizar la vista de eliminación. En este caso, es 'posts/eliminar_post.html'.
    '''
    template_name = 'posts/eliminar_post.html'
    
    '''
    Se especifica la URL a la que se redirigirá después de que se haya eliminado con éxito un objeto Post. reverse_lazy se utiliza para 
    invertir la URL basada en el nombre, en este caso, la URL llamada 'apps.posts:posts'.
    '''
    success_url = reverse_lazy('apps.posts:posts')

'''
e define la clase PostsPorCategoriaView, que hereda de ListView. Esto indica que esta vista se utilizará para mostrar una lista de objetos 
del modelo Post filtrados por una categoría específica.
'''       
class PostsPorCategoriaView(ListView):
    
    '''
    Se especifica el modelo cuyos objetos se mostrarán en la lista. En este caso, son objetos del modelo Post.
    '''
    model = Post
    
    '''
     Se especifica la plantilla que se utilizará para renderizar la vista. En este caso, es 'posts/posts_por_categoria.html'.
    '''
    template_name = 'posts/posts_por_categoria.html'
    
    '''
    Especifica el nombre del contexto que se utilizará en la plantilla para referenciar la lista de objetos Post. En la plantilla, 
    se puede acceder a esta lista utilizando el nombre 'posts'.
    '''
    context_object_name = 'posts'

    '''
    El método get_queryset se sobrescribe para proporcionar la lógica de obtener la lista de objetos Post filtrados por una categoría 
    específica. Utiliza el valor del parámetro pk de la URL para obtener la identificación de la categoría y luego filtra los objetos 
    Post por esa categoría.
    '''
    def get_queryset(self):
        categoria_id = self.kwargs['pk']
        return Post.objects.filter(categoria__id=categoria_id)
    
    '''
    El método get_context_data se sobrescribe para proporcionar datos adicionales al contexto de la plantilla. En este caso, añade 
    todas las categorías al contexto bajo el nombre 'categorias'. Esto puede ser útil para mostrar una lista de categorías en la interfaz de usuario.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
    
        
 
'''
Se define la clase CategoriaCreateView, que hereda de LoginRequiredMixin y de CreateView. Esto indica que esta vista requiere autenticación para 
acceder y que se utilizará para la creación de objetos del modelo Categoria.
'''     
class CategoriaCreateView(LoginRequiredMixin,CreateView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se crearán. En este caso, es el modelo Categoria.
    '''
    model = Categoria
    
    '''
    Se especifica la clase del formulario que se utilizará para recoger la información del usuario. En este caso, es la clase NuevaCategoriaForm.
    '''
    form_class = NuevaCategoriaForm
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista de creación de categoría. En este caso, es 'posts/crear_categoria.html'.
    '''
    template_name = 'posts/crear_categoria.html'
    
    '''
    se sobrescribe para proporcionar la URL a la que se redirigirá después de que se haya creado con éxito un nuevo objeto Categoria. Toma en cuenta 
    el parámetro opcional next en la URL, que podría ser utilizado para redirigir a la página anterior después de la creación exitosa. Si no se 
    proporciona una URL de redirección personalizada, se utiliza la URL especificada por reverse_lazy('apps.posts:crear_categoria').
    '''
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:crear_categoria')

'''
Se define la clase CategoriaListView, que hereda de ListView. Esto indica que esta vista se utilizará para mostrar una lista de objetos del modelo Categoria.
'''
class CategoriaListView(ListView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se mostrarán en la lista. En este caso, es el modelo Categoria.
    '''
    model = Categoria
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista. En este caso, es 'posts/categoria_list.html'.
    '''
    template_name = 'posts/categoria_list.html' 
    
    '''
     Especifica el nombre del contexto que se utilizará en la plantilla para referenciar la lista de objetos Categoria. 
     En la plantilla, se puede acceder a esta lista utilizando el nombre 'categorias'.
    '''
    context_object_name = 'categorias'
    
'''
Se define la clase CategoriaDeleteView, que hereda tanto de LoginRequiredMixin como de DeleteView. Esto indica que esta vista requiere autenticación para acceder y que se utilizará para la eliminación de objetos del modelo Categoria.
'''
class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se eliminarán. En este caso, es el modelo Categoria.
    '''
    model = Categoria
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista de confirmación de eliminación. En este caso, es 'posts/categoria_confirm_delete.html'.
    '''
    template_name = 'posts/categoria_confirm_delete.html'
    
    '''
    Se especifica la URL a la que se redirigirá después de que se haya eliminado con éxito un objeto Categoria. reverse_lazy se utiliza para invertir la URL basada en el nombre, en este caso, la URL llamada 'apps.posts:categoria_list'.
    '''
    success_url = reverse_lazy('apps.posts:categoria_list')

'''
Este código define una vista basada en clase en Django llamada ComentarioCreateView que utiliza la clase CreateView. Aquí hay una explicación detallada:
'''
class ComentarioCreateView(LoginRequiredMixin, CreateView):
        
        '''
          Especifica el modelo que se utilizará para crear nuevos objetos. 
          En este caso, se utilizará el modelo Comentario.
        '''
        model = Comentario
        
        '''
        Especifica la clase de formulario que se utilizará para la 
        entrada de datos. En este caso, se utilizará el formulario 
        ComentarioForm.
        '''
        form_class = ComentarioForm
        
        '''
        Especifica el nombre del archivo de plantilla que se utilizará 
        para renderizar la vista.
        '''
        template_name = 'comentario/crear_comentario.html'
        
        '''
        Especifica la URL a la que se redirigirá al usuario después de 
        que se haya creado con éxito un nuevo comentario. 
        '''
        success_url = 'comentario/comentarios/'
        
        '''
        El método form_valid es un método de la clase ComentarioCreateView 
        que hereda de la clase CreateView en Django. Este método se llama 
        cuando el formulario es válido y está a punto de ser procesado para 
        crear un nuevo objeto Comentario.
        '''
        def form_valid(self, form):
            
            '''
            Asigna el usuario actual (self.request.user) al campo usuario 
            del objeto Comentario. Esto se realiza antes de que el formulario 
            sea guardado, asegurando que el comentario tenga la información del 
            usuario que lo está creando.
            '''
            form.instance.usuario = self.request.user
            
            '''
            Asigna el identificador de la publicación actual (self.kwargs['posts_id']) 
            al campo posts_id del objeto Comentario. Esto utiliza los argumentos de la 
            URL (kwargs) para obtener el identificador de la publicación al que se 
            refiere este comentario.
            '''
            form.instance.posts_id = self.kwargs['posts_id']
            
            '''
            Llama al método form_valid de la clase base (super()) para realizar el 
            procesamiento estándar cuando el formulario es válido. Este método 
            generalmente se encarga de guardar el objeto en la base de datos y 
            realizar otras operaciones necesarias.
            '''
            return super().form_valid(form)

'''
Define una vista basada en clase en llamada ComentarioUpdateView que utiliza la clase UpdateView
'''
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se actualizarán. En este caso, es el modelo Comentario.
    '''
    model = Comentario
    
    '''
    Se especifica la clase del formulario que se utilizará para recoger la información del usuario.
    '''
    form_class = ComentarioForm
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista de actualización.
    '''
    template_name = 'comentario/comentario_form.html'
    
    '''
    e sobrescribe para proporcionar la URL a la que se redirigirá después de que se haya actualizado con éxito un 
    objeto Comentario. Toma en cuenta el parámetro opcional next en la URL, que podría ser utilizado para redirigir 
    a la página anterior después de la actualización exitosa. Si no se proporciona una URL de redirección personalizada, 
    se utiliza la URL generada utilizando reverse, que apunta a la vista de detalle individual de un post 
    ('apps.posts:post_individual') y pasa el ID del post actualizado como argumento en la URL.
    '''
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('apps.posts:post_individual', args=[self.object.posts.id])
        
'''
Define una vista basada en clase en Django llamada ComentarioDeleteView que utiliza la clase DeleteView.
'''
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    
    '''
    Se especifica el modelo al que pertenecen los objetos que se eliminarán. En este caso, es el modelo Comentario.
    '''
    model = Comentario
    
    '''
    Se especifica la plantilla que se utilizará para renderizar la vista de confirmación de eliminación.
    '''
    template_name = 'comentario/comentario_confirm_delete.html'
    
    '''
    Este método get_success_url se sobrescribe para proporcionar la URL a la que se redirigirá después de que se haya 
    eliminado con éxito un objeto Comentario. En este caso, se utiliza reverse para invertir la URL basada en el nombre 
    y se pasa el ID del post asociado al comentario como argumento en la URL. Esto redirige al usuario a la 
    vista individual de ese post.
    '''
    def get_success_url(self):
        return reverse('apps.posts:post_individual', args=[self.object.posts.id])
    
