from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
# from usuarios.models import usuarioL
from usuarios.models import UsuarioP
from usuarios.models import Registro, Acciones
from datetime import datetime
from .forms import RegistroConAccionesYPruebasForm, AccionForm, MensajeForm, AccionesForm, RegistroConAccionesFORM
from django.forms import inlineformset_factory

from datetime import date
@login_required
def dashboard(request):
    if request.method == 'GET':
        userDataI = UsuarioP.objects.filter(user__username=request.user)
        registrosConFechas = []
        dif = []

        if userDataI[0].tipo == "1":
            registros = Registro.objects.all().order_by('fecha_termino')
        else:
            registros_area = Registro.objects.filter(area=userDataI[0].OR).order_by('fecha_termino')
            registros_acciones_area2 = Registro.objects.filter(
                accionR__area2=userDataI[0].OR
            ).order_by('fecha_termino')

            registros = registros_area | registros_acciones_area2
            registros = registros.distinct()

        for registro in registros:
            fecha_inicio = registro.fecha_inicio.strftime('%d-%m-%Y')
            fecha_termino = registro.fecha_termino.strftime('%d-%m-%Y')
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
            fecha_termino_dt = datetime.strptime(fecha_termino, '%d-%m-%Y')
            diferencia = datetime.now() - fecha_termino_dt

            areas = registro.area.all()
            areas_str = ', '.join(area.nickname for area in areas)
            dias = diferencia.days

            registrosConFechas.append({
                'registro': registro,
                'fecha_inicio': fecha_inicio,
                'fecha_termino': fecha_termino,
                'diferencia': dias,
                'areas_str': areas_str,
            })

        context = {
            'registrosConFechas': registrosConFechas,
            'dataU': userDataI,
        }

        return render(request, "dashboard/dashboard.html", context)


def crear_registro(request):
    if request.method == 'POST':
        registro_form = RegistroConAccionesYPruebasForm(request.POST)
        if registro_form.is_valid():
            registro = registro_form.save()

            areas2 = registro_form.cleaned_data['accion1_area2']

            accion = Acciones.objects.create(
                descripcion=request.POST['accion1_descripcion']
            )
            accion.area2.set(areas2)
            accion.save()
            registro.accionR.add(accion)

            # prueba = Pruebas.objects.create(
            #     nom_archivo=request.POST['prueba1_nom_archivo'],
            #     tipo=request.POST['prueba1_tipo'],
            #     archivo_url=request.POST['prueba1_archivo_url']
            # )
            # prueba.acciones.add(accion)

            return redirect('dashboard')
    else:
        registro_form = RegistroConAccionesYPruebasForm()

    return render(request, 'dashboard/crear_registro.html', {
        'registro_form': registro_form,
    })



@login_required
def detalles(request, registro_id):
    registro = Registro.objects.get(pk=registro_id)
    mensajes = registro.mensajes.all().order_by('fecha_envio')
    userDataI = UsuarioP.objects.filter(user__username=request.user)

    for mensaje in mensajes:
        if mensaje.archivo:
            mensaje.archivo_nombre = mensaje.archivo.name.split('/')[-1]

    if request.method == 'POST':
        mensaje_form = MensajeForm(request.POST, request.FILES)
        if mensaje_form.is_valid():
            nuevo_mensaje = mensaje_form.save(commit=False)
            nuevo_mensaje.registro = registro
            nuevo_mensaje.usuario = request.user
            nuevo_mensaje.save()
            return redirect('detalles', registro_id=registro_id)
    else:
        mensaje_form = MensajeForm()

    context = {
        'registro': registro,
        'mensajes': mensajes,
        'mensaje_form': mensaje_form,
        'dataU': userDataI,
    }

    return render(request, 'dashboard/detalles.html', context)


@login_required
def editar_registro(request, id):
    registro = get_object_or_404(Registro, idRegistro=id)
    accion = registro.accionR.first()
    
    if request.method == 'POST':
        registro_form = RegistroConAccionesFORM(request.POST, instance=registro)
        accion_form = AccionesForm(request.POST, instance=accion)
        
        if registro_form.is_valid() and accion_form.is_valid():
            registro.fecha_finalizacion = "1970-01-01"
            registro = registro_form.save()
            accion = accion_form.save(commit=False)
            accion.save()
            registro.accionR.set([accion])
            
            registro.save()

            return redirect('dashboard')
    else:
        registro_form = RegistroConAccionesFORM(instance=registro)
        accion_form = AccionesForm(instance=accion)

    return render(request, 'dashboard/editar_registro.html', {
        'registro_form': registro_form,
        'accion_form': accion_form,
    })

@login_required
def eliminar_registro(request, idRegistro):
    registro = get_object_or_404(Registro, idRegistro=idRegistro)
    accion = registro.accionR.first()

    if request.method == 'POST':
        registro.delete()
        accion.delete()
        return redirect('dashboard')

    return render(request, 'dashboard/eliminar_registro.html', {'registro': registro})
