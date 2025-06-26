from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import random
from django.views import View

from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Usuario, Empresa, Rol, Clasificacion, Nivel



from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .models import Producto


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirige si ya está logueado

    if request.method == 'POST':
        correo = request.POST.get('correo_claro')
        password = request.POST.get('password')

        user = authenticate(request, correo_claro=correo, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'login.html')

#Logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión



from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    is_admin = request.user.rol.nombre.lower() == "admin"
    # Excluir empresa con id=1 en la lista de empresas
    empresas = Empresa.objects.exclude(id=1) if is_admin else [request.user.empresa]

    user_name = request.user.nombre


    selected_empresa_id = request.GET.get('empresa')
    mostrar_todas = is_admin and (not selected_empresa_id or selected_empresa_id == 'todas')

    if mostrar_todas:
        # Excluir empresa id=1 en productos
        productos_qs = Producto.objects.exclude(empresa_id=1)
    else:
        try:
            # Si es admin, obtener empresa seleccionada pero excluyendo la 1
            if is_admin:
                empresa_actual = Empresa.objects.exclude(id=1).get(pk=selected_empresa_id)
            else:
                empresa_actual = request.user.empresa
        except Empresa.DoesNotExist:
            empresa_actual = request.user.empresa
        
        # Solo productos de empresa_actual y nunca empresa 1
        productos_qs = Producto.objects.filter(empresa=empresa_actual).exclude(empresa_id=1)

    # Datos para gráfico de línea
    productos_por_fecha = (
        productos_qs
        .annotate(mes=TruncMonth('fecha_ingreso'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    line_chart_data = {
        'fechas': [item['mes'].strftime('%Y-%m') for item in productos_por_fecha],
        'totales': [item['total'] for item in productos_por_fecha]
    }

    # Gráfico pastel: Top 10 productos más pesados
    top_productos_pesados = (
        productos_qs
        .order_by('-peso')[:10]
        .values('nombre', 'peso')
    )

    pie_chart_data = [
        {'name': item['nombre'], 'value': float(item['peso'])}
        for item in top_productos_pesados
    ]

    # Totales
    total_productos = productos_qs.count()
    total_peso = productos_qs.aggregate(total=Sum('peso'))['total'] or 0

    base_template = 'sidebaradmin.html' if is_admin else 'sidebaruser.html'

    return render(request, 'home.html', {
        'base_template': base_template,
        'line_chart_data': line_chart_data,
        'pie_chart_data': pie_chart_data,
        'total_productos': total_productos,
        'total_peso': float(total_peso),
        'empresas': empresas,
        'is_admin': is_admin,
        'selected_empresa_id': selected_empresa_id or 'todas',
        'user_name': user_name,
    })




class RecuperarContrasenaView(View):
    template_name = 'recuperar_contra.html'

    def get(self, request):
        return render(request, self.template_name, {'step': 1})

    def post(self, request):
        step = int(request.POST.get('step'))

        if step == 1:
            correo = request.POST.get('correo_claro')
            try:
                usuario = Usuario.objects.get(correo_claro=correo)
                codigo = str(random.randint(10000, 99999))
                usuario.codigo_verificacion = codigo
                usuario.save()

                # Enviar correo
                send_mail(
                    subject='Código de verificación',
                    message=f'Tu código es: {codigo}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[correo],
                )

                request.session['correo_reset'] = correo
                return render(request, self.template_name, {'step': 2})

            except Usuario.DoesNotExist:
                messages.error(request, 'Correo no encontrado.')
                return render(request, self.template_name, {'step': 1})

        elif step == 2:
            codigo = request.POST.get('codigo')
            correo = request.session.get('correo_reset')

            try:
                usuario = Usuario.objects.get(correo_claro=correo)
                if usuario.codigo_verificacion == codigo:
                    return render(request, self.template_name, {'step': 3})
                else:
                    messages.error(request, 'Código incorrecto.')
                    return render(request, self.template_name, {'step': 2})
            except Usuario.DoesNotExist:
                messages.error(request, 'Correo no válido.')
                return redirect('login')

        elif step == 3:
            nueva_pass = request.POST.get('password')
            confirmar_pass = request.POST.get('password2')
            correo = request.session.get('correo_reset')

            if nueva_pass != confirmar_pass:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, self.template_name, {'step': 3})

            try:
                usuario = Usuario.objects.get(correo_claro=correo)
                usuario.set_password(nueva_pass)
                usuario.codigo_verificacion = None
                usuario.save()
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('login')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no válido.')
                return redirect('login')
    
