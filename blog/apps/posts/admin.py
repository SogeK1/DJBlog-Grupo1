from django.contrib import admin
from .models import Categoria, Post, Comentario

# Register your models here.

@admin.register(Post) #registro de clase

# declaramos una clase Para luego poder 
# usar un "list_display" con los atributos 
# que queramos mostrar en el panel admin
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'subtitulo', 'fecha', 'texto',
                    'activo', 'categoria', 'imagen', 'publicado',)
    
#registro de clase     
admin.site.register(Categoria)

#registro de clase     
admin.site.register(Comentario)