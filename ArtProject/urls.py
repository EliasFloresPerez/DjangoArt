"""
URL configuration for ArtProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from Aplicaciones.Header.views import login_view,home_view, RecuperarContrasenaView,logout_view
from Aplicaciones.Usuarios.views import UsuarioCrudView
from Aplicaciones.Niveles.views import NivelCrudView
from Aplicaciones.Clasificacion.views import ClasificacionCrudView
from Aplicaciones.Empresa.views import EmpresaCrudView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # URL para cerrar sesión
    path('home/', home_view, name='home'),
    path('recuperar/', RecuperarContrasenaView.as_view(), name='recuperar_contrasena'),
    path('usuarios/', UsuarioCrudView.as_view(), name='usuarios_crud'),  # URL para CRUD de usuarios
    path('niveles/', NivelCrudView.as_view(), name='niveles_crud'),  # URL para CRUD de niveles
    path('clasificacion/', ClasificacionCrudView.as_view(), name='clasificaciones_crud'),  # URL para CRUD de clasificaciones
    path('empresas/', EmpresaCrudView.as_view(), name='empresa_crud'),  # URL para CRUD de empresas

    

]

# Redirige cualquier URL no definida a la página principal (home)
urlpatterns += [
    path('<path:path>/', lambda request, path: redirect('home')),  # Ruta comodín
]
