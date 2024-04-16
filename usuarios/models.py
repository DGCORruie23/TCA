from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 

# Create your models here.
class Area(models.Model):
    idArea = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length = 100)

    def __str__(self):
        return  " {idArea}, {nickname}".format(idArea = self.idArea, nickname = self.nickname)

class Rubro(models.Model):
    idRubro = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length = 100)

    def __str__(self):
        return  " {idRubro}, {tipo}".format(idRubro = self.idRubro, tipo = self.tipo)

class Registro(models.Model):
    
    types_estado = [
        ("1", "En proceso"),
        ("2", "Atendido"),
    ]

    idRegistro = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, default="2")
    area = models.ManyToManyField(Area, related_name='registroA')
    estado = models.CharField(max_length=1, choices=types_estado, default="1")

    def __str__(self):
        return "{idRegistro}, {fecha_inicio}, {fecha_termino}, {rubro}, {estado}".format(idRegistro = self.idRegistro, 
                                                                      fecha_inicio = self.fecha_inicio, 
                                                                      fecha_termino = self.fecha_termino, 
                                                                      rubro = self.rubro,
                                                                      estado = self.estado)
    
class registroA(models.Model):
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    Area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return "{registro}, {area}".format(registro = self.registro, area = self.Area)

class Acciones(models.Model):
    idAccion = models.AutoField(primary_key=True)
    idRegistro = models.ManyToManyField(Registro, related_name='accionR')
    area1 = models.ManyToManyField(Area, related_name='accionA1')
    area2 = models.ManyToManyField(Area, related_name='accionA2')
    descripcion = models.TextField()

    def __str__(self):
        return "{idAccion}, {idRegistro}, {area1}, {area2}, {descripcion}".format(idAccion = self.idAccion, 
                                                                      idRegistro = self.idRegistro, 
                                                                      area1 = self.area1, 
                                                                      area2 = self.area2,
                                                                      descripcion = self.descripcion)

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
        return  " {idPruebas}, {nom_archivo}, {tipo}, {archivo_url}. {acciones}".format(idPruebas = self.idPruebas, nombreArchivo = self.nom_archivo, tipo = self.tipo, url = self.archivo_url , acciones = self.acciones)

class usuarioL(models.Model):
    user = models.OneToOneField(User, related_name="usuarioL", on_delete=models.CASCADE)
    area = models.ManyToManyField(Area, related_name='usuarioA')

    def __str__(self):
        print(self.area)
        return  " {nombre}, {area}".format(nombre = self.user, area = self.area)


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
        ("2", "Validador"),
        ("3", "Capturador"),
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