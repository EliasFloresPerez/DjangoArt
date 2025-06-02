# views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..Header.models import Nivel
from .forms import NivelForm

from ..Usuarios.mixins import AdminRequiredMixin 

class NivelCrudView(AdminRequiredMixin, View):
    template_name = 'Niveles.html'  # tu template principal

    def get(self, request, *args, **kwargs):
        niveles = Nivel.objects.exclude(id=1)

        form = NivelForm()

        context = {
            'niveles': niveles,
            'form': form,
            'base_template': 'sidebaradmin.html' 
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        nivel_id = request.POST.get('id')

        if action == 'create':
            form = NivelForm(request.POST)
            if form.is_valid():
                form.save()

        elif action == 'edit' and nivel_id:
            nivel = get_object_or_404(Nivel, pk=nivel_id)
            if nivel.id != 1:
                form = NivelForm(request.POST, instance=nivel)
                if form.is_valid():
                    form.save()

        elif action == 'delete' and nivel_id:
            nivel = get_object_or_404(Nivel, pk=nivel_id)
            if nivel.id != 1:
                nivel.delete()

        return redirect('niveles_crud')
