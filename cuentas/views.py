#from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from allauth.account.utils import complete_signup
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)    # cambiar
from django.contrib.auth import get_user_model
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
)    # cambiar
from django.urls import reverse    # Apéndice

from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView
)    # Apéndice

User = get_user_model()

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "cuentas/signup.html"
    success_url = reverse_lazy("articulos:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=raw_pw)  # Adjust based on your auth backend
        
        if user is not None:
            login(self.request, user)
            # Redirect to success_url after login
            return redirect(self.success_url)
        else:
            # Handle authentication failure
            return self.form_invalid(form)

# de aquí
class UserDetail(DetailView):
    model = User
    template_name = 'cuentas/user_detail.html'
# Hasta aquí
class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'cuentas/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})

class PasswordChange(PasswordChangeView):
    template_name = 'cuentas/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'cuentas/user_detail.html'

class UserDelete(DeleteView):
    model = User
    template_name = 'cuentas/user_delete.html'
    success_url = reverse_lazy('login')

class LogoutConfirmView(TemplateView):
    template_name = 'cuentas/logout_confirm.html'

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        # Recupera el id_token de la sesión del usuario
        client_id = getattr(settings, 'KEYCLOAK_CLIENT_ID', '')
        
        # Cierra la sesión en Django
        auth_logout(request)

        if client_id:
            logout_url = getattr(settings, 'LOGOUT_REDIRECT_URL', '')
        else:
            # Si no hay id_token, redirige al login normal
            logout_url = reverse("login")
        
        # Redirige al usuario a la URL de logout de Keycloak
        return redirect(logout_url)