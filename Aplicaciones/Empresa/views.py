from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..Header.models import Empresa
from ..Usuarios.mixins import AdminRequiredMixin
from .forms import EmpresaForm



class EmpresaCrudView(AdminRequiredMixin, View):
    template_name = 'Empresas.html'

    def get(self, request, *args, **kwargs):
        empresas = Empresa.objects.all()
        form = EmpresaForm()

        context = {
            'base_template': 'sidebaradmin.html',
            'empresas': empresas,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        empresa_id = request.POST.get('id')

        if action == 'create':
            form = EmpresaForm(request.POST)
            print(form)
            print(form.errors)
            if form.is_valid():
                
                form.save()

        elif action == 'edit' and empresa_id:
            empresa = get_object_or_404(Empresa, pk=empresa_id)
            form = EmpresaForm(request.POST, instance=empresa)
            if form.is_valid():
                form.save()

        elif action == 'delete' and empresa_id:
            empresa = get_object_or_404(Empresa, pk=empresa_id)
            empresa.delete()

        return redirect('empresa_crud')
