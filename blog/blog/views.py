from django.shortcuts import render
from django.http import HttpResponseNotFound

# Vista index
def index(request):
    return render(request,'index.html')

def pagina_404(request, exception):
    return HttpResponseNotFound('<h1>Página no encontrada<h1>')

