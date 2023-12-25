from django.shortcuts import render
from django.http import HttpResponseNotFound

'''
Esta vista simple llamada index renderiza la plantilla 'index.html' en respuesta 
a una solicitud. Es común tener una vista como esta para la página principal de un sitio web.
'''
def index(request):
    return render(request,'index.html')

'''
Esta vista pagina_404 maneja las solicitudes que resultan en un error 404 y devuelve una página con el mensaje 
"Página no encontrada". Puedes personalizar aún más esta vista según tus necesidades, incluyendo la posibilidad 
de usar una plantilla HTML.
'''
def pagina_404(request, exception):
    return HttpResponseNotFound('<h1>Página no encontrada<h1>')

