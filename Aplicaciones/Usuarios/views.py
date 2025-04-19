from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.hashers import make_password
from ..Header.models import Usuario
from .mixins import AdminRequiredMixin  # Usa el mixin que definimos antes


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Usuario
        fields = ['correo_claro', 'nombre', 'cedula', 'telefono', 'password', 'empresa', 'rol']

class UsuarioCrudView(AdminRequiredMixin, View):
    template_name_base = 'Usuario.html'

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        form = UsuarioForm()  # Formulario vacío para crear un nuevo usuario

        context = {
            'base_template': 'sidebaradmin.html',
            'usuarios': usuarios,
            'form': form
        }
        return render(request, self.template_name_base, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user_id = request.POST.get('id')

        if action == 'create':
            form = UsuarioForm(request.POST)

            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.correo = form.cleaned_data['correo_claro']

                # Si se ha proporcionado una nueva contraseña, la encriptamos
                if form.cleaned_data['password']:
                    usuario.password = make_password(form.cleaned_data['password'])
                else:
                    # Si no se proporciona contraseña, dejamos el valor como None
                    usuario.password = None

                usuario.save()

        elif action == 'edit' and user_id:
            usuario = get_object_or_404(Usuario, pk=user_id)
            form = UsuarioForm(request.POST, instance=usuario)
            usuario_original = Usuario.objects.get(pk=user_id)
            if form.is_valid():
                print('Formulario válido')
                
                usuario = form.save(commit=False)
                usuario.correo = form.cleaned_data['correo_claro']
                print('contraseña:', form.cleaned_data['password'])
                # Si se ha proporcionado una nueva contraseña, la encriptamos y si no paso nada '' la dejamos igual
                if form.cleaned_data['password'] != '':
                    print('Contraseña nueva:', form.cleaned_data['password'])
                    usuario.password = make_password(form.cleaned_data['password'])
                else:
                    # Si no se proporciona contraseña, dejamos el valor como None
                    usuario.password = usuario_original.password


                usuario.save()

        elif action == 'delete' and user_id:
            print('Eliminar usuario con ID:', user_id)
            usuario = get_object_or_404(Usuario, pk=user_id)
            usuario.delete()

        return redirect('usuarios_crud')