from django.urls import path
from . import views
from .views import LoginUsuario, LogoutUsuario
from django.contrib.auth import views as auth_views

'''
Define el espacio de nombres de la aplicación. Esto se utiliza para diferenciar las URL de diferentes aplicaciones en un proyecto Django. 
En este caso, parece ser una aplicación llamada 'usuario'.
'''
app_name = 'apps.usuario'

'''
Aquí se definen las rutas para diversas vistas. Cada ruta está vinculada a una vista específica. Algunas rutas están vinculadas a vistas 
de autenticación proporcionadas por Django, mientras que otras están vinculadas a vistas personalizadas definidas en el código.
'''
urlpatterns = [
    path('registrar/', views.RegistrarUsuario.as_view(), name='registrar'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutUsuario.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/<int:pk>/eliminar', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]
'''
En resumen, este código configura las rutas para diferentes vistas en la aplicación. Las rutas están relacionadas con la autenticación 
de usuarios y otras operaciones relacionadas con usuarios, como registrar nuevos usuarios, iniciar sesión, cerrar sesión, etc. También hay 
rutas para operaciones personalizadas como listar usuarios y eliminar usuarios.
'''