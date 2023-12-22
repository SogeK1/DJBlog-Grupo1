from django import template


'''
Aquí se crea una instancia de template.Library() y se asigna a la 
variable register. Este objeto se utiliza para registrar los 
filtros personalizados y las etiquetas de las plantillas.
'''
register = template.Library()

'''
Esta línea utiliza el decorador @register.filter para registrar la función 
has_group como un filtro de plantilla. El parámetro name='has_group' 
especifica el nombre del filtro que se utilizará en las plantillas.
'''
@register.filter(name='has_group')

# Esta es la definición de la función has_group que toma dos parámetros: user y
# group_name. user representa un objeto de usuario de Django, y group_name es el
# nombre del grupo que se verificará.
def has_group(user, group_name):
    
    '''
     Esta línea verifica si el usuario pertenece al grupo especificado. 
     user.groups.filter(name=group_name) filtra los grupos del usuario por el 
     nombre del grupo, y .exists() devuelve True si hay al menos un grupo que 
     coincide, lo que indica que el usuario pertenece al grupo.
    '''
    return user.groups.filter(name=group_name).exists()
