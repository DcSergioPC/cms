#from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
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
    form_class = CustomUserCreationForm   # cambiar
    template_name = "cuentas/signup.html"
    success_url = reverse_lazy("articulos:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_pw)
        login(self.request, user)
        return response

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