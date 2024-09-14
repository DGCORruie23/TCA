from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.models import Registro, Acciones, Notificacion, Area, Rubro, UsuarioP
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear

@login_required
def general(request):
    if request.method == 'GET':
        userDataI = UsuarioP.objects.filter(user__username=request.user)
        registros = Registro.objects.all()
        consultarAreas = Area.objects.all()
        consultarRubros = Rubro.objects.all()
        nombres_areas = [area.nickname for area in consultarAreas]
        # lista_años = [str(año) for año in range(2020, datetime.now().year + 1)]
        lista_años = range(2020, datetime.now().year + 1)

        # registros_OR = registros.values('area').annotate(total= Count('idRegistro'))
        # registros_OR_year = registros.values('area', year=ExtractYear('fecha_inicio')).annotate(total= Count('idRegistro')).order_by('area', 'year')

        # for registro in registros_OR:
        #     print(f"{consultarAreas.filter(idArea=registro['area']).first().name}  TOTAL {registro['total']}")

        # for registro in registros_OR_year:
        #     print(f"Área: {consultarAreas.filter(idArea=registro['area']).first().name}, Año: {registro['year']}, Total registros: {registro['total']}")
        
        registro_V_A = []
        visitasT = 0
        acuerdosT = 0
        pendientesT = 0
        atenditosT = 0

        #Tabla 1
        registros_visitas = registros.values('area', 'fecha_inicio').annotate(total= Count('idRegistro')).order_by('area', 'fecha_inicio')

        for registro in registros_visitas:
            # print(f"OR: {consultarAreas.filter(idArea=registro['area']).first().name} Fecha: {registro['fecha_inicio']} TOTAL {registro['total']}")
            registro_V_A.append({
                'area': str(consultarAreas.filter(idArea=registro['area']).first().name).replace("OR ",""),
                'fecha': datetime.strftime(registro['fecha_inicio'], "%d/%m/%Y"),
                'total': registro['total']
            })



        # registros_years = registros.values( "fecha_inicio", year=ExtractYear('fecha_inicio')).annotate(
        #tabla 2
        registros_years = registros.values(year=ExtractYear('fecha_inicio')).annotate(
            total_registros=Count('idRegistro'),
            total_fechas_unicas=Count('fecha_inicio', distinct=True),
            total_pendi=Count('idRegistro', filter=Q(estado="1")), 
            total_aten=Count('idRegistro', filter=Q(estado="2")), 
            ).order_by('year')
        

        #tabla 3
        registros_rubros = (registros.values("rubro", year=ExtractYear('fecha_inicio'))
             .annotate(total_unico=Count('rubro'))
             .order_by("rubro", 'year'))
        # registros_rubros = registros.values( "rubro",year=ExtractYear('fecha_inicio')).annotate(
        #     total_unico=Count('rubro'),
        #     ).order_by("rubro",'year')

        data_by_rubro = {}
        for registro in registros_rubros:
            # rubro = registro['rubro']
            rubro = consultarRubros.filter(idRubro=registro["rubro"]).first().tipo
            yearT = registro['year']
            total = registro['total_unico']
            
            if rubro not in data_by_rubro:
                data_by_rubro[rubro] = {year: 0 for year in lista_años}
            
            # Actualizar el año con el total correcto
            data_by_rubro[rubro][yearT] = total

        # print(data_by_rubro)

        # for registro in registros_rubros:
        #     print(f"Año: {registro["year"]}, Rubro: {consultarRubros.filter(idRubro=registro["rubro"]).first().tipo }, Acuerdos: {registro["total_unico"]}")

        for registro in registros_years:
            visitasT += registro['total_fechas_unicas']
            acuerdosT += registro['total_registros']
            pendientesT += registro['total_pendi']
            atenditosT += registro['total_aten']
            
            # print(
            #     "Año: {year}, Visitas: {visitas}, Pendientes: {pendientes}, Atendidos: {atendidos}, Totales: {totales}".format(
            #         year= registro['year'],
            #         visitas= registro['total_fechas_unicas'],
            #         pendientes= registro['total_pendi'],
            #         atendidos= registro['total_aten'],
            #         totales= registro['total_registros'],
            #     )
            # )
            # print(f"Año: {registro['year']}, visitas: {registro['total_fechas_unicas']} Pendientes: {registro['total_atendidos']}, ,  Total acuerdos: {registro['total_registros']}")
        

        infoTabla= []
        
        context = {
            "tabla1" : registro_V_A,
            "tabla2" : registros_years,
            "tabla3" : data_by_rubro,
            "visitas": visitasT,
            "acuerdos": acuerdosT,
            "years": lista_años,
        }
        return render(request, "estadistica/informacion.html", context)

