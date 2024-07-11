from django.contrib import admin

from .models import Registro, Area, Rubro,  Acciones, UsuarioP

# registroA, usuarioA, accionR, accionA1, accionA2, accionP

# admin.site.register(usuarioL)
admin.site.register(Registro)
admin.site.register(Area)
admin.site.register(Rubro)
admin.site.register(UsuarioP)
admin.site.register(Acciones)
# admin.site.register(accionR)
# admin.site.register(accionA1)
# admin.site.register(accionA2)
# admin.site.register(Pruebas)
# admin.site.register(accionP)
# admin.site.register(registroA)
# admin.site.register(usuarioA)

# Register your models here.

# from django.contrib import admin
# from .models import Usuario

# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('idUser', 'nickname', 'nombre', 'apellido', 'estado', 'tipo')
#     list_filter = ('estado', 'tipo')
#     search_fields = ('nickname', 'nombre', 'apellido')
#     # Especifica los campos editables en el formulario de edición
#     fields = ('nickname', 'nombre', 'apellido', 'estado', 'tipo')

# admin.site.register(Usuario, UsuarioAdmin)
