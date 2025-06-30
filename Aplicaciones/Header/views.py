from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import random
from django.views import View

from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Usuario, Empresa, Rol, Clasificacion, Nivel, Producto, Categoria



from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from .models import RAEE  # Si tienes un modelo RAEE, descomenta y ajusta


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
    

@csrf_exempt
def chatbot_api(request):
    # Verificar que solo usuarios admin puedan acceder
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autorizado'}, status=401)
    
    # Verificar si es admin
    if request.user.rol.nombre.lower() != "admin":
        return JsonResponse({'error': 'Acceso denegado. Solo administradores pueden usar el chatbot.'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        
        # Usar la misma lógica de filtrado que el dashboard
        is_admin = request.user.rol.nombre.lower() == "admin"
        
        if is_admin:
            # Para admin, contar todos los productos excepto empresa 1
            total_productos = Producto.objects.exclude(empresa_id=1).count()
        else:
            # Para usuario normal, solo productos de su empresa
            total_productos = Producto.objects.filter(empresa=request.user.empresa).exclude(empresa_id=1).count()
        
        response = process_raee_message(message, total_productos, request.user)
        
        return JsonResponse({'response': response})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def process_raee_message(message, total_productos, user):
    # Lógica del chatbot con datos reales del sistema
    if 'estadísticas' in message or 'stats' in message or 'cuántos' in message:
        # Usar la misma lógica de filtrado que el dashboard
        is_admin = user.rol.nombre.lower() == "admin"
        
        if is_admin:
            total_peso = Producto.objects.exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
        else:
            total_peso = Producto.objects.filter(empresa=user.empresa).exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
        
        return f"📊 Tu sistema tiene registrados {total_productos} productos RAEE con un peso total de {float(total_peso):.2f} kg."
    
    if 'empresa' in message and ('cuántos' in message or 'por empresa' in message):
        # Consultar productos por empresa
        productos_por_empresa = Producto.objects.values('empresa__nombre').annotate(
            total=Count('id'),
            peso_total=Sum('peso')
        ).exclude(empresa_id=1).order_by('-total')
        
        if productos_por_empresa:
            respuesta = "🏢 **RAEE por empresa:**\n"
            for item in productos_por_empresa:
                empresa_nombre = item['empresa__nombre']
                total = item['total']
                peso = float(item['peso_total'] or 0)
                respuesta += f"• **{empresa_nombre}**: {total} productos ({peso:.1f} kg)\n"
            return respuesta
        else:
            return "No hay productos RAEE registrados por empresa aún."
    
    if 'año' in message or 'ano' in message or 'year' in message:
        # Mostrar opciones de años disponibles
        from datetime import datetime
        current_year = datetime.now().year
        
        # Usar la misma lógica de filtrado que el dashboard
        is_admin = user.rol.nombre.lower() == "admin"
        
        respuesta = f"📅 **Selecciona un año para ver los RAEE:**\n"
        for year in range(2022, current_year + 1):
            # Contar productos por año
            if is_admin:
                productos_anio = Producto.objects.filter(fecha_ingreso__year=year).exclude(empresa_id=1).count()
                peso_anio = Producto.objects.filter(fecha_ingreso__year=year).exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
            else:
                productos_anio = Producto.objects.filter(fecha_ingreso__year=year, empresa=user.empresa).exclude(empresa_id=1).count()
                peso_anio = Producto.objects.filter(fecha_ingreso__year=year, empresa=user.empresa).exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
            
            respuesta += f"• **{year}**: {productos_anio} productos ({float(peso_anio):.1f} kg)\n"
        
        return respuesta
    
    if 'impacto' in message or 'ambiental' in message or 'co2' in message:
        # Usar la misma lógica de filtrado que el dashboard
        is_admin = user.rol.nombre.lower() == "admin"
        
        if is_admin:
            total_peso = Producto.objects.exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
        else:
            total_peso = Producto.objects.filter(empresa=user.empresa).exclude(empresa_id=1).aggregate(Sum('peso'))['peso__sum'] or 0
        
        co2_saved = float(total_peso) * 2.5
        agua_saved = float(total_peso) * 15
        return f"🌱 Con {float(total_peso):.2f} kg de RAEE reciclado has evitado:\n• {co2_saved:.1f} kg de CO₂\n• {agua_saved:.0f} litros de agua\n• Recuperado materiales valiosos"
    
    if 'categorías' in message or 'categorias' in message or 'tipos' in message:
        categorias = Categoria.objects.all()
        if categorias:
            cat_list = "\n".join([f"• {cat.codigo}: {cat.descripcion}" for cat in categorias[:5]])
            return f"📋 Las categorías disponibles son:\n{cat_list}"
        else:
            return "No hay categorías registradas aún."
    
    if 'empresas' in message or 'empresa' in message:
        empresas = Empresa.objects.exclude(id=1).count()
        return f"🏢 Hay {empresas} empresas registradas en el sistema."
    
    if 'registrar' in message or 'nuevo' in message or 'agregar' in message:
        return "Para registrar un nuevo RAEE:\n1️⃣ Ve a 'Productos' en el menú\n2️⃣ Haz clic en 'Agregar'\n3️⃣ Completa los datos del producto\n4️⃣ Guarda el registro"
    
    if 'beneficios' in message or 'ventajas' in message:
        return "♻️ Los beneficios de reciclar RAEE incluyen:\n• Reducción de contaminación\n• Recuperación de metales preciosos\n• Ahorro de energía\n• Cumplimiento normativo\n• Responsabilidad ambiental"
    
    if 'ayuda' in message or 'como' in message:
        return "🤖 Puedo ayudarte con:\n• Estadísticas del sistema\n• RAEE por empresa\n• RAEE por año\n• Impacto ambiental\n• Categorías de RAEE\n• Proceso de registro\n• Información de empresas"
    
    # Respuesta por defecto
    return "Interesante pregunta 🤔 Puedo ayudarte con estadísticas, RAEE por empresa, RAEE por año, impacto ambiental, categorías, registro de productos y más."
    