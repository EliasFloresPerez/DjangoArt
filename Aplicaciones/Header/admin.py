from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Empresa, Rol, Nivel, Clasificacion, Categoria, Producto
from .forms import UsuarioCreationForm, UsuarioChangeForm

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm

    list_display = ('correo_claro', 'nombre', 'rol', 'empresa', 'is_active')
    list_filter = ('rol', 'empresa', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('correo_claro', 'password')}), 
        ('Datos personales', {'fields': ('nombre', 'telefono', 'cedula')}),  # Aquí se pide la cédula en texto claro
        ('Empresa y Rol', {'fields': ('empresa', 'rol')}), 
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo_claro', 'nombre', 'cedula', 'telefono', 'empresa', 'rol', 'password1', 'password2'),
        }),
    )

    search_fields = ('correo_claro',)
    ordering = ('correo_claro',)

    def save_model(self, request, obj, form, change):
        obj.correo = obj.correo_claro  # Guardamos el correo normal
        obj.cedula = obj.cedula  # Esto usará el setter para encriptar la cédula
        obj.telefono = obj.telefono  # Guardamos el teléfono directamente
        super().save_model(request, obj, form, change)

# Registros de otros modelos
admin.site.register(Empresa)
admin.site.register(Rol)
admin.site.register(Nivel)
admin.site.register(Clasificacion)
admin.site.register(Categoria)
admin.site.register(Producto)
