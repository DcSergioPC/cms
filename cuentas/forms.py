from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms    # Apéndice



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'age')


# de aquí
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
        )

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']  # Asegúrate de que 'role' esté en tu modelo CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí podrías agregar lógica adicional para el formulario si es necesario

# Hasta aquí