from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..Header.models import Producto, Usuario, Empresa
from .forms import ProductoForm
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.db.models import Sum

from .CrearPDF import generar_pdf_retiro_raee_bytes
from .CrearCSV import generar_excel_retiro_raee_bytes
from django.http import HttpResponse


class ProductoCrudView(LoginRequiredMixin, View):
    template_name = 'Productos.html'
    
    def get_queryset(self, request):
        if request.user.rol.nombre.lower() == 'admin':
            return Producto.objects.select_related('empresa', 'categoria').all()
        else:
            return Producto.objects.filter(empresa=request.user.empresa)

    def get(self, request, *args, **kwargs):
        productos = self.get_queryset(request)
        form = ProductoForm()
        #Nombre de usuario
        user_name = request.user.nombre

        context = {
            'base_template': 'sidebaradmin.html' if request.user.rol.nombre.lower() == 'admin' else 'sidebaruser.html',
            'productos': productos,
            'form': form,
            'user_name': user_name,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        producto_id = request.POST.get('id')

        try:
            if action == 'create':
                form = ProductoForm(request.POST)
                if form.is_valid():
                    producto = form.save(commit=False)
                    if request.user.rol.nombre.lower() != 'admin':
                        producto.empresa = request.user.empresa
                    producto.save()
                    messages.success(request, "Producto creado exitosamente.")
                else:
                    messages.error(request, "Error al crear producto. Verifica los campos.")

            elif action == 'edit' and producto_id:
                producto = get_object_or_404(Producto, pk=producto_id)
                if request.user.rol.nombre.lower() != 'admin' and producto.empresa != request.user.empresa:
                    return redirect('producto_crud')

                form = ProductoForm(request.POST, instance=producto)
                if form.is_valid():
                    producto = form.save(commit=False)
                    if request.user.rol.nombre.lower() != 'admin':
                        producto.empresa = request.user.empresa
                    producto.save()
                    messages.success(request, "Producto actualizado exitosamente.")
                else:
                    print(form.errors)
                    messages.error(request, "Error al actualizar producto.")

            elif action == 'delete' and producto_id:
                producto = get_object_or_404(Producto, pk=producto_id)
                if request.user.rol.nombre.lower() == 'admin' or producto.empresa == request.user.empresa:
                    producto.delete()
                    messages.success(request, "Producto eliminado correctamente.")
                else:
                    messages.error(request, "No tienes permisos para eliminar este producto.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado: {e}")

        return redirect('producto_crud')


class Reporte(View):
    def post(self, request, *args, **kwargs):
        tipo_filtro = request.POST.get('tipo_filtro')  # empresa, categoria, origen, estado
        tipo_reporte = request.POST.get('tipo_reporte')  # 'csv' o 'pdf'
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        tituloReporte = request.POST.get('titulo')
        
        

        ids = request.POST.getlist('productos_seleccionados')
        productos = Producto.objects.filter(id__in=ids)
        
        
        fecha_inicio_obj = parse_date(fecha_inicio) if fecha_inicio else None
        fecha_fin_obj = parse_date(fecha_fin) if fecha_fin else None

        # Base queryset
        #productos = Producto.objects.all()

        print("Tipo de filtro:", tipo_filtro)
        # Filtrar por rango de fechas si está definido
        if fecha_inicio_obj and fecha_fin_obj:
            productos = productos.filter(fecha_ingreso__range=(fecha_inicio_obj, fecha_fin_obj))

        # Agrupar y sumar según el tipo de filtro
        if tipo_filtro == 'empresa':
            agrupado = productos.values('empresa__nombre').annotate(total_peso=Sum('peso'))
        elif tipo_filtro == 'categoria':
            agrupado = productos.values('categoria__descripcion').annotate(total_peso=Sum('peso'))
        elif tipo_filtro == 'origen':
            agrupado = productos.values('origen').annotate(total_peso=Sum('peso'))
        elif tipo_filtro == 'estado':
            agrupado = productos.values('estado').annotate(total_peso=Sum('peso'))
        else:
            messages.error(request, "Debe seleccionar un filtro válido.")
            return redirect('producto_crud')

        if not agrupado:
            messages.error(request, "No se encontraron productos para el filtro seleccionado.")
            return redirect('producto_crud')

        #Cambios la clave de agrupacion para generar los reportes 
        if tipo_filtro == 'empresa':
            for p in agrupado:
                p["Datos"] = p.pop("empresa__nombre")
        elif tipo_filtro == 'categoria':
            for p in agrupado:
                p["Datos"] = p.pop("categoria__descripcion")
        elif tipo_filtro == 'origen':
            for p in agrupado:
                p["Datos"] = p.pop("origen")
        elif tipo_filtro == 'estado':
            for p in agrupado:
                p["Datos"] = p.pop("estado")

        # Enviar a la función de generación del reporte según tipo
        if tipo_reporte == 'csv':
            messages.success(request, f"Reporte generado correctamente ({tipo_reporte.upper()})")
            return self.generar_csv(tituloReporte, agrupado, tipo_filtro)
        elif tipo_reporte == 'pdf':
            messages.success(request, f"Reporte generado correctamente ({tipo_reporte.upper()})")
            return self.generar_pdf(tituloReporte, agrupado, tipo_filtro)
        else:
            messages.error(request, "Tipo de reporte no válido.")
            return redirect('producto_crud')
        

    def generar_csv(self, titulo, productos, filtro):

        for p in productos:
            print(p)
        output = generar_excel_retiro_raee_bytes(productos, titulo, filtro)
        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="reporte_raee.xlsx"'
        return response

    def generar_pdf(self, titulo, productos, filtro):
        output = generar_pdf_retiro_raee_bytes(productos, titulo, filtro)
        response = HttpResponse(output, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reporte_raee.pdf"'
        return response
