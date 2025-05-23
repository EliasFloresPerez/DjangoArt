from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..Header.models import Producto, Usuario, Empresa
from .forms import ProductoForm

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
        context = {
            'base_template': 'sidebaradmin.html' if request.user.rol.nombre.lower() == 'admin' else 'sidebaruser.html',
            'productos': productos,
            'form': form
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

class ReporteCSV(View):
    def post(self, request, *args, **kwargs):


        ids = request.POST.getlist('productos_seleccionados')
        productos = Producto.objects.filter(id__in=ids)

        if not productos.exists():
            messages.error(request, "No se seleccionaron productos para el reporte. CSV")
            return redirect('producto_crud')
        
        print("\n🖨️ Productos seleccionados CSV:")
        for p in productos:
            print(f"- ID: {p.id}, Nombre: {p.nombre}, Código: {p.codigo}, Empresa: {p.empresa.nombre}")

        messages.success(request, f"Se imprimieron {productos.count()} productos en la consola del servidor. CSV")
        return redirect('producto_crud')


#Reporte PDF
class ReportePDF(View):
    def post(self, request, *args, **kwargs):


        ids = request.POST.getlist('productos_seleccionados')
        productos = Producto.objects.filter(id__in=ids)

        if not productos.exists():
            messages.error(request, "No se seleccionaron productos para el reporte. PDF")
            return redirect('producto_crud')
        
        print("\n🖨️ Productos seleccionados PDF:")
        for p in productos:
            print(f"- ID: {p.id}, Nombre: {p.nombre}, Código: {p.codigo}, Empresa: {p.empresa.nombre}")

        messages.success(request, f"Se imprimieron {productos.count()} productos en la consola del servidor. PDF")
        return redirect('producto_crud')

