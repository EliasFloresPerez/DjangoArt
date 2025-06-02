from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..Header.models import Clasificacion
from .forms import ClasificacionForm  # si lo pusiste en forms.py
from ..Usuarios.mixins import AdminRequiredMixin  # si querés protegerla como hiciste con Usuario

class ClasificacionCrudView(AdminRequiredMixin, View):
    template_name = 'clasificaciones.html'

    def get(self, request, *args, **kwargs):
        clasificaciones = Clasificacion.objects.select_related('nivel').exclude(id=1)

        form = ClasificacionForm()
        
        context = {
            'base_template': 'sidebaradmin.html',
            'clasificaciones': clasificaciones,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        clasificacion_id = request.POST.get('id')

        if action == 'create':
            form = ClasificacionForm(request.POST)
            if form.is_valid():
                form.save()

        elif action == 'edit' and clasificacion_id:
            clasificacion = get_object_or_404(Clasificacion, pk=clasificacion_id)
            if clasificacion.id != 1:
                form = ClasificacionForm(request.POST, instance=clasificacion)
                if form.is_valid():
                    form.save()

        elif action == 'delete' and clasificacion_id:
            clasificacion = get_object_or_404(Clasificacion, pk=clasificacion_id)
            if clasificacion.id != 1:
                clasificacion.delete()

        return redirect('clasificaciones_crud')
