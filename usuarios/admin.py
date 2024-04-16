from django.contrib import admin

from .models import usuarioL, Registro, Area, Rubro, Pruebas, Acciones, registroA

admin.site.register(usuarioL)
admin.site.register(Registro)
admin.site.register(Area)
admin.site.register(Rubro)
admin.site.register(Acciones)
admin.site.register(Pruebas)
admin.site.register(registroA)

# Register your models here.
