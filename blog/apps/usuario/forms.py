from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate, login

'''
RegistroUsuarioForm hereda de UserCreationForm, que es un formulario 
proporcionado por Django para la creación de usuarios.
En la clase Meta, se especifica que este formulario se asocia con el modelo Usuario.
La lista fields determina qué campos se mostrarán en el formulario. En este caso, se incluyen campos como 
'username', 'first_name', 'last_name', ' 'password1', 'password2', 'email', y 'imagen'.
'''
class RegistroUsuarioForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'imagen']



'''
LoginForm es un formulario que se utiliza para la autenticación de usuarios.
Se definen dos campos, 'username' y 'password', utilizando forms.CharField y forms.PasswordInput respectivamente.
El método login es personalizado y se utiliza para realizar la autenticación del usuario en el sistema.
Dentro del método login, se obtienen los datos limpios (cleaned_data) del formulario y se utiliza la función 
authenticate para verificar las credenciales del usuario.
Si el usuario es autenticado con éxito, se utiliza la función login para iniciar sesión en el sistema.
'''
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
  
    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
