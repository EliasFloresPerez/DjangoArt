from django.contrib import admin

# Register your models here.

from .models import Usuario, Empresa, Rol, Nivel, Clasificacion, Categoria, Producto

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Rol)
admin.site.register(Nivel)
admin.site.register(Clasificacion)
admin.site.register(Categoria)
admin.site.register(Producto)


