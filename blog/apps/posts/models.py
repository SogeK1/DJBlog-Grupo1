from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

# Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.nombre
    
# Post
class Post(models.Model):
    """
    Representa un post.

    Attributes:
        titulo: El título del post.
        subtitulo: El subtítulo opcional del post.
        fecha: La fecha y hora de creación del post.
        texto: El texto del post.
        activo: Indica si el post está activo.
        categoria: La categoría del post.
        imagenes: Las imágenes del post.
        publicado: La fecha y hora de publicación del post.
    """

    titulo = models.CharField(max_length=50, null=False)
    subtitulo = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default='Sin categoría')
    imagen = models.FileField(null=True, blank=True, upload_to='media', default='static/post_default.png')
    publicado = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        '''
        los objetos de la clase Post se devolverán en orden descendente por la fecha de publicación. 
        Esto significa que los objetos más recientes se devolverán primero.
        '''
        ordering = ('-publicado',)
    
    '''
    Formatea el titulo en string
    '''
    def __str__(self):
        return (self.titulo)
    
    # Borrar registros de la db por defecto, en los modelos hijo y padre.
    def delete(self, using = None, keep_parents = False):
        self.imagen.delete(self.imagen.name)
        super().delete()
    
'''
Este modelo Comentario representa un comentario asociado a un Post y a un usuario. 
Almacena información como el texto del comentario, la fecha de creación y las 
relaciones con el post y el usuario correspondientes.
'''
class Comentario(models.Model):
    posts = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return self.texto
    