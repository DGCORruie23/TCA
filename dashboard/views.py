from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# from usuarios.models import usuarioL
from usuarios.models import UsuarioP
from usuarios.models import Registro, Acciones, Notificacion,Area, Rubro
from datetime import datetime, timedelta, timezone
from .forms import RegistroConAccionesYPruebasForm, MensajeForm, AccionesForm, RegistroConAccionesFORM, CargarArchivoForm
from django.forms import inlineformset_factory
import openpyxl as opxl

from datetime import date
from datetime import datetime
import re

from dateutil.parser import parse
@login_required
def dashboard(request):
    if request.method == 'GET':
        userDataI = UsuarioP.objects.filter(user__username=request.user)
        registrosConFechas = []
        formCargar1 = CargarArchivoForm()
        if userDataI[0].tipo == "1":
            registros = Registro.objects.all().order_by('fecha_termino')
        else:
            registros_area = Registro.objects.filter(area=userDataI[0].OR).order_by('fecha_termino')
            registros_acciones_area2 = Registro.objects.filter(
                accionR__area2=userDataI[0].OR
            ).order_by('fecha_termino')

            registros = registros_area | registros_acciones_area2
            registros = registros.distinct().order_by('fecha_termino')

        registros_en_proceso = registros.filter(estado="1")
        registros_atendidos = registros.filter(estado="2")

        registros_ordenados = list(registros_en_proceso) + list(registros_atendidos)

        for registro in registros_ordenados:
            fecha_inicio = registro.fecha_inicio.strftime('%d-%m-%Y')
            fecha_termino = registro.fecha_termino.strftime('%d-%m-%Y')
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
            fecha_termino_dt = datetime.strptime(fecha_termino, '%d-%m-%Y')
            diferencia = datetime.now() - fecha_termino_dt
            fecha_finalizacion = registro.fecha_finalizacion
            areas = registro.area.all()
            areas_str = ', '.join(area.nickname for area in areas)
            areas_name = ', '.join(area.name for area in areas)
            dias = diferencia.days

            registrosConFechas.append({
                'registro': registro,
                'fecha_inicio': fecha_inicio,
                'fecha_termino': fecha_termino,
                'diferencia': dias,
                'areas_str': areas_str,
                'areas_name': areas_name,
                'fecha_finalizacion': fecha_finalizacion
            })

        now = datetime.now()
        nuevos_registros = registros.filter(fecha_creacion__gte=now - timedelta(days=7))


        for registro in nuevos_registros:
            Notificacion.objects.get_or_create(user=request.user, registro=registro)

        notificaciones = Notificacion.objects.filter(user=request.user, leido=False)

        context = {
            'registrosConFechas': registrosConFechas,
            'dataU': userDataI,
            'notificaciones': notificaciones,
            'formCargar1': formCargar1,
        }

        return render(request, "dashboard/dashboard.html", context)

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, user=request.user)
    notificacion.leido = True
    notificacion.fecha_leido = datetime.now()
    notificacion.save()
    return redirect('dashboard')

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
            if registro.estado == 1:
                registro.fecha_finalizacion = "1970-01-01"
            else:
                registro.fecha_finalizacion = datetime.now().strftime("%Y-%m-%d")
            
            registro = registro_form.save()
            accion = accion_form.save()
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







MONTHS = {
    'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
    'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
    'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
}

def convert_spanish_date(date_str):
    if isinstance(date_str, str):
        match = re.match(r'(\d{1,2}) de (\w+) de (\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            month_number = {
                'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
                'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
            }.get(month.lower())
            if month_number:
                return datetime(int(year), month_number, int(day)).date()
    return None

from datetime import datetime

@login_required
@csrf_exempt
def cargaMasiva(request):
    if request.method == "POST":
        form = CargarArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["archivo"]
            nombreA = str(excel_file.name)
            extensionA = (nombreA.split(".")[-1]).lower()

            if extensionA in ["xlsx", "xlsm", "xlsb", "xltx", "xltm", "xls"]:
                dataWB = opxl.load_workbook(excel_file, data_only=True)
                data = dataWB.worksheets[0]

                i = 1
                while True:
                    if data.cell(i + 4, 4).value is None:
                        break

                    clave_acuerdo = data.cell(i + 4, 1).value
                    rubro = data.cell(i + 4, 2).value
                    descripcion = data.cell(i + 4, 3).value  # Este campo no se usa en Registro
                    areas_responsables = data.cell(i + 4, 4).value
                    fecha_termino = data.cell(i + 4, 5).value
                    fecha_inicio = data.cell(i + 4, 6).value
                    or_field = data.cell(i + 4, 7).value
                    estado = data.cell(i + 4, 8).value
                    fecha_finalizacion = data.cell(i + 4, 9).value

                    # Convertir fechas
                    fecha_inicio = convert_spanish_date(fecha_inicio) if isinstance(fecha_inicio, str) else fecha_inicio
                    if fecha_termino == "De manera inmediata":
                        fecha_termino = fecha_inicio
                    else:
                        fecha_termino = convert_spanish_date(fecha_termino) if isinstance(fecha_termino, str) else fecha_termino

                    fecha_finalizacion = convert_spanish_date(fecha_finalizacion) if isinstance(fecha_finalizacion, str) else fecha_finalizacion
                    if fecha_finalizacion is None:
                        fecha_finalizacion = datetime(1970, 1, 1).date()

                    if clave_acuerdo and clave_acuerdo.count('/') == 2:
                        partes = clave_acuerdo.split('/')
                        clave_acuerdo = f"{partes[1]}/{partes[0]}/{partes[2]}"

                    rubro_obj, created = Rubro.objects.get_or_create(tipo=rubro)
                    areas_responsables_list = areas_responsables.split(',')
                    areas_objs = []
                    for area in areas_responsables_list:
                        area_obj, created = Area.objects.get_or_create(nickname=area.strip())
                        areas_objs.append(area_obj)

                    # Actualizar solo los campos válidos
                    registro, created = Registro.objects.update_or_create(
                        claveAcuerdo=clave_acuerdo,
                        defaults={
                            "fecha_inicio": fecha_inicio,
                            "fecha_termino": fecha_termino,
                            "estado": estado,
                            "fecha_finalizacion": fecha_finalizacion,
                        }
                    )
                    registro.rubro.set([rubro_obj])
                    registro.area.set(areas_objs)

                    i += 1

            return redirect("dashboard")
    else:
        form = CargarArchivoForm()
    return render(request, "dashboard/dashboard.html", {"form": form})
