from django.contrib import admin

from .models import Registro, Area, Rubro,  Acciones, UsuarioP, Mensaje, Notificacion

admin.site.register(Registro)
admin.site.register(Area)
admin.site.register(Rubro)
admin.site.register(UsuarioP)
admin.site.register(Acciones)
admin.site.register(Mensaje)
admin.site.register(Notificacion)