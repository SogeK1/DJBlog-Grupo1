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

'''
Aquí se define una nueva clase llamada CrearPostForm que hereda de forms.ModelForm. 
Esta clase se utiliza para crear un formulario basado en el modelo Post.
'''
class CrearPostForm(forms.ModelForm):
    
    '''
    Dentro de la clase CrearPostForm, se define una clase interna llamada Meta. 
    La clase Meta se utiliza para proporcionar metadatos asociados al formulario.
    '''
    class Meta:
        
        '''
        Se especifica el modelo al que está vinculado el formulario.
        '''
        model = Post
        
        '''
        Indica que se deben incluir todos los campos del modelo en el formulario. 
        En otras palabras, el formulario contendrá campos para todos los campos del modelo Post.
        '''
        fields = '__all__'

'''
Aquí se define una nueva clase llamada NuevaCategoriaForm que hereda de forms.ModelForm. 
Esta clase se utiliza para crear un formulario basado en el modelo Categoria.
'''
class NuevaCategoriaForm(forms.ModelForm):
    
    '''
    Dentro de la clase CrearPostForm, se define una clase interna llamada Meta. 
    La clase Meta se utiliza para proporcionar metadatos asociados al formulario.
    '''
    class Meta:
        
        '''
        Se especifica el modelo al que está vinculado el formulario.
        '''
        model = Categoria
        
        '''
        Indica que se deben incluir todos los campos del modelo en el formulario. 
        En otras palabras, el formulario contendrá campos para todos los campos del modelo Post.
        '''
        fields = '__all__'
        
