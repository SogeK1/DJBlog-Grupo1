from django import forms
from .models import Comentario, Post, Categoria


'''
Define una nueva clase llamada ComentarioForm que 
hereda de forms.ModelForm. Esta clase se utilizará 
para crear formularios basados en el modelo Comentario.
'''
class ComentarioForm(forms.ModelForm):
    '''
    Dentro de la clase ComentarioForm, se define una clase interna Meta, 
    que se utiliza para proporcionar metadatos asociados al formulario.
    '''
    class Meta:
        '''
        Especifica el modelo que se utilizará para construir el formulario. 
        En este caso, el formulario se basará en el modelo Comentario.
        '''
        model = Comentario
        '''
        Indica los campos del modelo que deben incluirse en el formulario. 
        En este caso, solo se incluirá el campo texto del modelo Comentario.
        '''
        fields = ['texto']
class CrearPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class NuevaCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        
