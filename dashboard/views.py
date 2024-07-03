from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from usuarios.models import usuarioL
from usuarios.models import Usuario
from usuarios.models import Registro, Acciones, Pruebas
from datetime import datetime
from .forms import RegistroConAccionesYPruebasForm, AccionForm, PruebaForm
from django.forms import inlineformset_factory



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
            diferencia = datetime.now() - fecha_termino_dt
            print(diferencia)
            dias = diferencia.days
            dif.append(dias)

        registrosConFechas = zip(registrosConFechas, dif)
        

        pruebas = Pruebas.objects.all()
        
        context = {
            'registrosConFechas': registrosConFechas,
            'pruebas': pruebas,
        }

        return render(request, "dashboard/dashboard.html", context)

# def crear_registro(request):
#     if request.method == 'POST':
#         form = RegistroForm(request.POST)
#         if form.is_valid():
#             registro = form.save()  

#             return redirect('dashboard') 
#     else:
#         form = RegistroForm()
#     return render(request, 'dashboard/crear_registro.html', {'form': form})


def crear_registro(request):
    if request.method == 'POST':
        registro_form = RegistroConAccionesYPruebasForm(request.POST)
        print("Entró al POST")
        if registro_form.is_valid():
            print("Registro es válido")
            registro = registro_form.save(commit=False)  # Guardamos el formulario pero no lo enviamos a la base de datos todavía
            registro.save()

            # Guardamos las áreas seleccionadas
            areas1 = registro_form.cleaned_data['accion1_area1']
            areas2 = registro_form.cleaned_data.get('accion1_area2', [])  # Puede ser None si no hay selecciones

            # Creamos la acción
            accion = Acciones.objects.create(
                descripcion=request.POST['accion1_descripcion']
            )

            # Asignamos las áreas a la acción
            accion.area1.add(*areas1)
            accion.area2.add(*areas2)
            print(accion)
            # Guardamos la acción
            accion.save()

            # Relacionamos la acción con el registro
            registro.accionR.add(accion)

            # Creamos la prueba
            prueba = Pruebas.objects.create(
                nom_archivo=request.POST['prueba1_nom_archivo'],
                tipo=request.POST['prueba1_tipo'],
                archivo_url=request.POST['prueba1_archivo_url']
            )

            # Relacionamos la prueba con la acción
            prueba.acciones.add(accion)

            # Redireccionamos al dashboard u otra página
            return redirect('dashboard')
        else:
            print("Registro form es inválido")
            print(registro_form.errors)  # Esto imprimirá los errores del formulario en la consola
    else:
        registro_form = RegistroConAccionesYPruebasForm()

    return render(request, 'dashboard/crear_registro.html', {
        'registro_form': registro_form,
    })




# def editar_registro(request, registro_id):
#     registro = get_object_or_404(Registro, idRegistro=registro_id)
    
#     if request.method == 'POST':
#         registro_form = RegistroConAccionesYPruebasForm(request.POST, instance=registro)
#         if registro_form.is_valid():
#             registro = registro_form.save(commit=False)

#             areas1 = registro_form.cleaned_data['accion1_area1']
#             areas2 = registro_form.cleaned_data['accion1_area2']

#             accion = Acciones.objects.create(
#                 descripcion=request.POST['accion1_descripcion']
#             )
#             accion.area1.set(areas1)
#             accion.area2.set(areas2)
#             accion.save()
#             registro.accionR.add(accion)

#             prueba = Pruebas.objects.create(
#                 nom_archivo=request.POST['prueba1_nom_archivo'],
#                 tipo=request.POST['prueba1_tipo'],
#                 archivo_url=request.POST['prueba1_archivo_url']
#             )
#             prueba.acciones.add(accion)

#             return redirect('dashboard')
#     else:
#         registro_form = RegistroConAccionesYPruebasForm(instance=registro)

#     return render(request, 'dashboard/editar_registro.html', {
#         'registro_form': registro_form,
#         'registro_id': registro_id,
#     })


def editar_registro(request, registro_id):

    registro = get_object_or_404(Registro, idRegistro=registro_id)
    data = {
        'form': registro
    }
    if request.method == 'POST':
        print("Entró al POST")
        formulario = RegistroConAccionesYPruebasForm(data = request.POST, instance=registro)

        if formulario.is_valid():
            print("Entró a la validación")
            formulario.save()
            data['message'] = "Datos Modificados correctamente"
            data['form'] = formulario
            return redirect('dashboard')
        else:
            print("Entró al ELSE")
            print(formulario.errors)



    return render(request, 'dashboard/editar_registro.html', context= data)


def detalles(request,registro_id):

    return render(request,'dashboard/detalles.html')