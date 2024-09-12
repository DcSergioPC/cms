Cuentas
=======

Modelos
-------

**Descripción de Clases de models.py**

- CustomUser

.. code-block:: python

   class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    age = models.PositiveIntegerField(('Age'), default=0, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    data_joined = models.DateTimeField(_('data joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

Definicion de usuario personalizado con CustomUser

Funcionalidades de permisos y grupos. Verificacion de permisos de usuario con PermissionsMixin

El campo username es el nombre de usuario, para la autentificacion se utiliza email, USERNAME_FIELD

El campo email es para la direccion de correo electronico (es unica)

El método clean() es para limpiar y normalizar los datos del modelo antes de guardarlos

El método email_user() es para enviar un correo electrónico al usuario. send_mail de Django se utiliza para enviar el correo

..
   .. automodule:: cuentas.models
   :members:
   :undoc-members:
   :show-inheritance:

Vistas
------
..
   .. automodule:: cuentas.views
   :members:
   :undoc-members:
   :show-inheritance:

Formularios
-----------

**Descripción de Clases de forms.py**

- CustomUserCreationForm

.. code-block:: python

   class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'age')

CustomUserCreationForm(UserCreationForm) define un usuario con datos personalizados (formulario personalizado). Extiende de la clase UserCreationForm. Se permite agregar campos a la descripcion de usuario

Con Meta(UserCreationForm.Meta) se define la estructura del formulario

Se definen los campos del formulario mediante fields = UserCreationForm.Meta.fields + ('email', 'age')

- UserUpdateForm

.. code-block:: python

   class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
        )

Para actualizar la informacion del usuario (UserUpdateForm) se define un formulario que hereda de ModelForm

Se define estructuracion de formulario con clase Meta

El formulario esta basado en el modelo CustomUser mediante model = CustomUser

Se definen los campos que estan en el formulario con fields = (
            'username',
            'email',
            'age',
        )

..
   .. automodule:: cuentas.forms
   :members:
   :undoc-members:
   :show-inheritance:
