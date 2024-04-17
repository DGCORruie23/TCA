from django.contrib import admin

from .models import usuarioL, Registro, Area, Rubro, Pruebas, Acciones

# registroA, usuarioA, accionR, accionA1, accionA2, accionP

admin.site.register(usuarioL)
admin.site.register(Registro)
admin.site.register(Area)
admin.site.register(Rubro)
admin.site.register(Acciones)
# admin.site.register(accionR)
# admin.site.register(accionA1)
# admin.site.register(accionA2)
admin.site.register(Pruebas)
# admin.site.register(accionP)
# admin.site.register(registroA)
# admin.site.register(usuarioA)

# Register your models here.
