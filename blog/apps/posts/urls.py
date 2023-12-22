from django.urls import path
from .views import *

'''
La variable app_name se utiliza para definir un espacio de nombres para las URL de la aplicación. 
En este caso, se establece en 'apps.contacto', lo que significa que las URLs de esta aplicación 
deben tener un prefijo que coincida con este espacio de nombres.
'''
app_name = 'apps.posts'

# Este código define un conjunto de URLconf para una aplicación.
urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_individual'),
    path('post/', PostCreateView.as_view(), name='crear_post'),
    path('post/categoria', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('post/<int:pk>/modificar', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/eliminar', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/editar', ComentarioUpdateView.as_view(), name='comentario_editar'),
    path('post/<int:pk>/comentario_eliminar', ComentarioDeleteView.as_view(), name='comentario_eliminar'),
    path('categoria/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/<int:pk>/delete/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('categoria/<int:pk>/posts/', PostsPorCategoriaView.as_view(), name='posts_por_categoria'),
    
]
'''
Estas rutas y vistas forman la estructura básica de la aplicación y permiten realizar operaciones como ver, 
crear, editar y eliminar posts, categorías y comentarios. Además, hay algunas rutas que proporcionan 
funcionalidades específicas, como ver posts asociados a una categoría particular.
'''