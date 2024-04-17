from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User
from usuarios.models import usuarioL
from usuarios.models import Usuario
from usuarios.models import Registro, Acciones

# Create your views here.
@login_required
# def dashboard(request):

#     if request.method == 'GET':
#         data = Registro.objects.all()
#         acciones = Acciones.objects.all()
#         accionPruebas =  accionP.objects.all()
#         accionRegistro = accionR.objects.all()
#         print('hola')

#         print(data)

#         context = {
#             "registro": data,
#             "acciones": acciones,
#             "accionPruebas": accionPruebas,
#             "accionRegistro": accionRegistro,
#                 }
#         return render(request, "dashboard/dashboard.html")
    

def dashboard(request):
    if request.method == 'GET':
        # Obtener todos los registros
        registros = Registro.objects.all()
        # Pasar los registros al contexto
        context = {
            'registros': registros
        }
        # Renderizar el template con los registros
        return render(request, "dashboard/dashboard.html", context)
