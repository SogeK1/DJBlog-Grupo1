from django.apps import AppConfig

'''
Aquí se define una nueva clase llamada PostsConfig que 
hereda de AppConfig. Esta clase se utiliza para configurar la aplicación.
'''
class PostsConfig(AppConfig):

    '''
    Esta línea establece el campo automático predeterminado que se utilizará 
    para los modelos de esta aplicación. En este caso, se ha configurado con 
    'django.db.models.BigAutoField', que es una opción adecuada para bases de datos 
    que admiten campos de autoincremento grandes.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    
    '''
    Aquí se especifica el nombre de la aplicación. Antes de cambiarlo, el nombre de la 
    aplicación se establecería automáticamente según la ubicación del archivo de configuración. 
    Pero en este caso, se ha cambiado explícitamente a 'apps.posts'. Esta configuración es 
    especialmente útil cuando la aplicación no se encuentra en un paquete de nivel superior.
    '''
    name = 'apps.posts' # cambiado
