from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User
from usuarios.models import usuarioL
from usuarios.models import Usuario
from usuarios.models import Registro, Acciones, Pruebas
from datetime import datetime

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

        registros = Registro.objects.all().order_by('fecha_termino')

        registrosConFechas = []
        dif = []

        for registro in registros:
            fecha_inicio = registro.fecha_inicio.strftime('%d-%m-%Y')
            fecha_termino = registro.fecha_termino.strftime('%d-%m-%Y')
            registrosConFechas.append((registro, fecha_inicio, fecha_termino))

            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y') 
            fecha_termino_dt = datetime.strptime(fecha_termino, '%d-%m-%Y')
            diferencia = fecha_termino_dt - fecha_inicio_dt
            dias = diferencia.days
            dif.append(dias)

        registrosConFechas = zip(registrosConFechas, dif)
        

        pruebas = Pruebas.objects.all()
        
        context = {
            'registrosConFechas': registrosConFechas,
            'pruebas': pruebas,
        }

        return render(request, "dashboard/dashboard.html", context)




