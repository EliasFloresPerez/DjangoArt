# usuarios/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class AdminRequiredMixin(LoginRequiredMixin):
    """Permite acceso solo a usuarios cuyo rol sea 'admin' (según tu modelo de Rol)."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, 'rol') or request.user.rol.nombre.lower() != 'admin':
            return redirect('dashboard')  # Asegúrate que 'dashboard' exista en tus URLs

        return super().dispatch(request, *args, **kwargs)
