# views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..Usuarios.mixins import AdminRequiredMixin
from ..Header.models import Categoria
from .forms import CategoriaForm

class CategoriaCrudView(AdminRequiredMixin, View):
    template_name = 'Categorias.html'

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        form = CategoriaForm()

        context = {
            'base_template': 'sidebaradmin.html',
            'categorias': categorias,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        categoria_id = request.POST.get('id')

        if action == 'create':
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()

        elif action == 'edit' and categoria_id:
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()

        elif action == 'delete' and categoria_id:
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            categoria.delete()

        return redirect('categoria_crud')  # asegurate que el nombre coincida en urls.py
