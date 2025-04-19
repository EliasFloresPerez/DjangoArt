from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cryptography.fernet import Fernet
import base64
import os
from django.contrib import admin

# Generar y guardar esta clave de forma segura en producción
KEY = base64.urlsafe_b64encode(os.urandom(32))
fernet = Fernet(KEY)



class UsuarioManager(BaseUserManager):
    def create_user(self, correo_claro, password=None, **extra_fields):
        if not correo_claro:
            raise ValueError('El correo claro es obligatorio')
        
        correo_claro = self.normalize_email(correo_claro)

        user = self.model(correo_claro=correo_claro, **extra_fields)
        user.correo = correo_claro  # esto usa tu setter personalizado
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_claro, password=None, **extra_fields):
       
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if 'empresa' not in extra_fields:
            extra_fields['empresa'] = Empresa.objects.get(pk=1)

        if 'rol' not in extra_fields:
            extra_fields['rol'] = Rol.objects.get(pk=1)

        return self.create_user(correo_claro, password, **extra_fields)


# Empresa y demás modelos
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    actividad = models.CharField(max_length=200)

    def __str__(self):
        return self.actividad

class Clasificacion(models.Model):
    cod_actividad = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    actividad_economica = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200)
    representante = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ruc = models.CharField(max_length=20)
    clasificacion = models.ForeignKey(Clasificacion, on_delete=models.SET_NULL, null=True, unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    origen = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.nombre

class Usuario(AbstractBaseUser, PermissionsMixin):
    correo_encriptado = models.BinaryField()
    correo_claro = models.EmailField(unique=True)  # Este es el indexado para login
    cedula = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #Codigo de verificacion
    codigo_verificacion = models.CharField(max_length=10, blank=True, null=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_claro'  # usamos el campo visible
    REQUIRED_FIELDS = []

    @property
    def correo(self):
        return fernet.decrypt(self.correo_encriptado).decode()

    @correo.setter
    def correo(self, value):
        self.correo_encriptado = fernet.encrypt(value.encode())
        self.correo_claro = value  # también actualizamos el visible




    def __str__(self):
        return self.correo_claro


