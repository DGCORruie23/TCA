from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 

# Create your models here.
# class Area(models.Model):
#     idArea = models.AutoField(primary_key=True)
#     nickname = models.CharField(max_length = 100)

#     def __str__(self):
#         return  " {idArea}, {nickname}".format(idArea = self.idArea, nickname = self.nickname)

# class Rubro(models.Model):
#     idRubro = models.AutoField(primary_key=True)
#     tipo = models.CharField(max_length = 100)

#     def __str__(self):
#         return  " {idRubro}, {tipo}".format(idRubro = self.idRubro, tipo = self.tipo)

# class Registro(models.Model):
    
#     types_estado = [
#         ("1", "En proceso"),
#         ("2", "Atendido"),
#     ]

#     idRegistro = models.AutoField(primary_key=True)
#     fecha_inicio = models.DateField()
#     fecha_termino = models.DateField()
#     rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, default="2")
#     estado = models.CharField(max_length=1, choices=types_estado, default="1")

#     def __str__(self):
#         return "{idRegistro}, {fecha_inicio}, {fecha_termino}, {rubro}, {estado}".format(idRegistro = self.idRegistro, 
#                                                                       fecha_inicio = self.fecha_inicio, 
#                                                                       fecha_termino = self.fecha_termino, 
#                                                                       rubro = self.rubro,
#                                                                       estado = self.estado)
    
# class registroA(models.Model):
#     registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
#     Area = models.ForeignKey(Area, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{registro}, {area}".format(registro = self.registro, area = self.Area)

# class Acciones(models.Model):
#     idAccion = models.AutoField(primary_key=True)
#     descripcion = models.TextField()

#     def __str__(self):
#         return "{idAccion},{descripcion}".format(idAccion = self.idAccion, descripcion = self.descripcion)
# class accionR(models.Model):
#     idAccion = models.ForeignKey(Acciones, on_delete=models.CASCADE)
#     idRegistro = models.ForeignKey(registroA, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{idAccion}, {idRegistro}".format(idAccion = self.idAccion, idRegistro = self.idRegistro)
    
# class accionA1(models.Model):
#     idAccion = models.ForeignKey(Acciones, on_delete=models.CASCADE)
#     area1 = models.ForeignKey(Area, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{idAccion}, {area1}".format(idAccion = self.idAccion, area1 = self.area1)
    
# class accionA2(models.Model):
#     idAccion = models.ForeignKey(Acciones, on_delete=models.CASCADE)
#     area2 = models.ForeignKey(Area, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{idAccion}, {area2}".format(idAccion = self.idAccion, area2 = self.area2)

# class Pruebas(models.Model):
#     types_archivo = [
#         ("1", "URL"),
#         ("2", "Local"),
#     ]
#     idPruebas = models.AutoField(primary_key=True)
#     nom_archivo = models.TextField()
#     tipo = models.CharField(max_length=1, choices=types_archivo, default="1")
#     archivo_url = models.TextField()

#     def __str__(self):
#         return  " {idPruebas}, {nom_archivo}, {tipo}, {archivo_url}".format(idPruebas = self.idPruebas, nom_archivo = self.nom_archivo, tipo = self.tipo, archivo_url = self.archivo_url )

# class accionP(models.Model):
#     idPruebas = models.ForeignKey(Pruebas, on_delete=models.CASCADE)
#     idAccion = models.ForeignKey(Acciones, on_delete=models.CASCADE)

#     def __str__(self):
#         return " {idAccion},{idPruebas},".format(idAccion = self.idAccion, idPruebas = self.idPruebas)
    

class Area(models.Model):
    idArea = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=150)
    # abrevArea = models.CharField(max_length=15, default="abreviatura")

    def __str__(self):
        return f"{self.idArea},{self.nickname},"


class Rubro(models.Model):
    idRubro = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.idRubro}, {self.tipo}"


class Registro(models.Model):

    types_estado = [
        ("1", "En proceso"),
        ("2", "Atendido"),
    ]

    idRegistro = models.AutoField(primary_key=True)
    claveAcuerdo = models.TextField(default="Clave de Acuerdo")
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    rubro = models.ManyToManyField(Rubro, related_name='registroR')
    area = models.ManyToManyField(Area, related_name='registroA')
    estado = models.CharField(max_length=1, choices=types_estado, default="1")

    def __str__(self):
        return f"Registro: {self.idRegistro}, Clave de Acuerdo: {self.claveAcuerdo}, Fecha de inicio: {self.fecha_inicio}, Fecha de término: {self.fecha_termino}, Rubro: {', '.join([rubro.tipo for rubro in self.rubro.all()])}, Áreas: {', '.join([area.nickname for area in self.area.all()])}, Estado: {self.get_estado_display()}"


class Acciones(models.Model):
    idAccion = models.AutoField(primary_key=True)
    idRegistro = models.ManyToManyField(Registro, related_name='accionR')
    area2 = models.ManyToManyField(Area, related_name='accionA2')
    descripcion = models.TextField()

    def __str__(self):
        return f"Acción: {self.idAccion}, Registros: {', '.join([str(registro.idRegistro) for registro in self.idRegistro.all()])}, Área 2: {', '.join([area.nickname for area in self.area2.all()])}, Descripción: {self.descripcion}"


# class Pruebas(models.Model):
#     types_archivo = [
#         ("1", "URL"),
#         ("2", "Local"),
#     ]
#     idPruebas = models.AutoField(primary_key=True)
#     nom_archivo = models.TextField()
#     tipo = models.CharField(max_length=1, choices=types_archivo, default="1")
#     archivo_url = models.TextField()
#     acciones = models.ManyToManyField(Acciones, related_name='accionP')

#     def __str__(self):
#         return f"Prueba: {self.idPruebas}, Nombre de Archivo: {self.nom_archivo}, Tipo: {self.get_tipo_display()}, URL del Archivo: {self.archivo_url}, Acciones: {', '.join([str(accion.idAccion) for accion in self.acciones.all()])}"



# class usuarioL(models.Model):
#     user = models.OneToOneField(User, related_name="usuarioL", on_delete=models.CASCADE)

#     def __str__(self):
#         return  " {nombre}".format(nombre = self.user)
    
# class usuarioA(models.Model):
#     user = models.ForeignKey(usuarioL, on_delete=models.CASCADE)
#     Area = models.ForeignKey(Area, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{user}, {area}".format(user = self.user, area = self.Area)


class UsuarioP(models.Model):
    types_ORS = [
        ("1", "OR AGS"), ("2", "OR BC"), ("3", "OR BCS"), ("4", "OR CAMP"), ("5", "OR COAH"),
        ("6", "OR COL"), ("7", "OR CHIS"), ("8", "OR CHIH"), ("9", "OR CDMX"), ("10", "OR DGO"),
        ("11", "OR GTO"), ("12", "OR GRO"), ("13", "OR HGO"), ("14", "OR JAL"), ("15", "OR EDOMEX"),
        ("16", "OR MICH"), ("17", "OR MOR"), ("18", "OR NAY"), ("19", "OR NL"), ("20", "OR OAX"),
        ("21", "OR PUE"), ("22", "OR QRO"), ("23", "OR QROO"), ("24", "OR SLP"), ("25", "OR SIN"),
        ("26", "OR SON"), ("27", "OR TAB"), ("28", "OR TAMPS"), ("29", "OR TLX"), ("30", "OR VER"),
        ("31", "OR YUC"), ("32", "OR ZAC"), ("33", "DGTIC"), ("34", "DGCM"), ("35", "DGRAM"), ("36", "DG"), ("37", "SCJ"), ("38", "DGA"), ("39", "DGECCC"), ("40", "DGCOR"),
    ]


    types_user = [
        ("1" , "Administrador"),
        ("2", "Editor"),
    ]
    idUser = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="usuarioP", on_delete=models.CASCADE, default=1)
    nickname = models.CharField(max_length = 20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=200)
    # password = models.CharField(max_length=250)
    OR = models.CharField(max_length=2, choices=types_ORS, default="9")
    tipo = models.CharField(max_length=1, choices=types_user, default="3")
    
    def save(self, *args, **kwargs):
        # self.password = make_password(self.password)
        super(UsuarioP, self).save(*args, **kwargs)

    def __str__(self):
        return  " {id}, {nickname}, {state}, {type}".format(id = self.idUser, nickname = self.nickname, state = self.OR, type = self.tipo)