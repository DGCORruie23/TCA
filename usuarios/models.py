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
    abrevArea = models.CharField(max_length=15, default="abreviatura")

    def __str__(self):
        return f"{self.idArea}, {self.nickname},{self.abrevArea}"


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
        return f"Registro: {self.idRegistro}, Clave de Acuerdo: {self.claveAcuerdo}, Fecha de inicio: {self.fecha_inicio}, Fecha de término: {self.fecha_termino}, Rubro: {', '.join([rubro.tipo for rubro in self.rubro.all()])}, Áreas: {', '.join([area.abrevArea for area in self.area.all()])}, Estado: {self.get_estado_display()}"


class Acciones(models.Model):
    idAccion = models.AutoField(primary_key=True)
    idRegistro = models.ManyToManyField(Registro, related_name='accionR')
    area1 = models.ManyToManyField(Area, related_name='accionA1')
    area2 = models.ManyToManyField(Area, related_name='accionA2')
    descripcion = models.TextField()

    def __str__(self):
        return f"Acción: {self.idAccion}, Registros: {', '.join([str(registro.idRegistro) for registro in self.idRegistro.all()])}, Área 1: {', '.join([area.nickname for area in self.area1.all()])}, Área 2: {', '.join([area.nickname for area in self.area2.all()])}, Descripción: {self.descripcion}"


class Pruebas(models.Model):
    types_archivo = [
        ("1", "URL"),
        ("2", "Local"),
    ]
    idPruebas = models.AutoField(primary_key=True)
    nom_archivo = models.TextField()
    tipo = models.CharField(max_length=1, choices=types_archivo, default="1")
    archivo_url = models.TextField()
    acciones = models.ManyToManyField(Acciones, related_name='accionP')

    def __str__(self):
        return f"Prueba: {self.idPruebas}, Nombre de Archivo: {self.nom_archivo}, Tipo: {self.get_tipo_display()}, URL del Archivo: {self.archivo_url}, Acciones: {', '.join([str(accion.idAccion) for accion in self.acciones.all()])}"



class usuarioL(models.Model):
    user = models.OneToOneField(User, related_name="usuarioL", on_delete=models.CASCADE)

    def __str__(self):
        return  " {nombre}".format(nombre = self.user)
    
# class usuarioA(models.Model):
#     user = models.ForeignKey(usuarioL, on_delete=models.CASCADE)
#     Area = models.ForeignKey(Area, on_delete=models.CASCADE)

#     def __str__(self):
#         return "{user}, {area}".format(user = self.user, area = self.Area)


class Usuario(models.Model):
    types_ORS = [
        ("1", "AGUASCALIENTES"),
        ("2", "BAJA CALIFORNIA"),
        ("3", "BAJA CALIFORNIA SUR"),
        ("4", "CAMPECHE"),
        ("5", "COAHUILA"),
        ("6", "COLIMA"),
        ("7", "CHIAPAS"),
        ("8", "CHIHUAHUA"),
        ("9", "CDMX"),
        ("10", "DURANGO"),
        ("11", "GUANAJUATO"),
        ("12", "GUERRERO"),
        ("13", "HIDALGO"),
        ("14", "JALISCO"),
        ("15", "EDOMEX"),
        ("16", "MICHOACÁN"),
        ("17", "MORELOS"),
        ("18", "NAYARIT"),
        ("19", "NUEVO LEÓN"),
        ("20", "OAXACA"),
        ("21", "PUEBLA"),
        ("22", "QUERÉTARO"),
        ("23", "QUINTANA ROO"),
        ("24", "SAN LUIS POTOSÍ"),
        ("25", "SINALOA"),
        ("26", "SONORA"),
        ("27", "TABASCO"),
        ("28", "TAMAULIPAS"),
        ("29", "TLAXCALA"),
        ("30", "VERACRUZ"),
        ("31", "YUCATÁN"),
        ("32", "ZACATECAS"),
    ]
    types_user = [
        ("1" , "Administrador"),
        ("2", "Editor"),
    ]
    idUser = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length = 20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=200)
    password = models.CharField(max_length=250)
    estado = models.CharField(max_length=2, choices=types_ORS, default="9")
    tipo = models.CharField(max_length=1, choices=types_user, default="3")

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return  " {id}, {nickname}, {state}, {type}".format(id = self.idUser, nickname = self.nickname, state = self.estado, type = self.tipo)