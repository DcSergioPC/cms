.. cms documentation master file, created by
   sphinx-quickstart on Thu Sep  5 23:24:35 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================================================
Documentación del Sistema de Administración de Contenido - CMS
==============================================================

Equipo de trabajo
=================
- **Equipo 08**: [Equipo 08]
- ``Integrantes``:

  - Alexis Gastón Cañete Aguero  
  - Jesús Milciades Portillo Espinola  
  - Sergio Daniel Portillo Caballero  
  - David Alejandro Jimeneza Ariste  

Requisitos de desarrollo
========================
- Python 3.11.6
- Django==5.1
- PostgreSQL 16

A través del comando ``pip install -r requirements.txt`` se instalan:

- anyio==4.4.0
- alabaster==1.0.0
- asgiref==3.8.1
- async-property==0.2.2
- certifi==2024.8.30
- cffi==1.17.0
- charset-normalizer==3.3.2
- deprecation==2.1.0
- babel==2.16.0
- colorama==0.4.6
- cryptography==43.0.0
- Django==5.1
- django-allauth==64.2.0
- gunicorn==20.1.0
- h11==0.14.0
- httpcore==1.0.5
- httpx==0.27.2
- idna==3.8
- jwcrypto==1.5.6
- packaging==24.1
- docutils==0.21.2
- imagesize==1.4.1
- Jinja2==3.1.4
- MarkupSafe==2.1.5
- pillow==10.4.0
- psycopg==3.2.1
- psycopg-binary==3.2.1
- psycopg2==2.9.9
- pycparser==2.22
- PyJWT==2.9.0
- Pygments==2.18.0
- python-dotenv==1.0.1
- python-keycloak==4.3.0
- requests==2.32.3
- requests-toolbelt==1.0.0
- sniffio==1.3.1
- snowballstemmer==2.2.0
- Sphinx==8.0.2
- sphinxcontrib-applehelp==2.0.0
- sphinxcontrib-devhelp==2.0.0
- sphinxcontrib-htmlhelp==2.1.0
- sphinxcontrib-jsmath==1.0.1
- sphinxcontrib-qthelp==2.0.0
- sphinxcontrib-serializinghtml==2.0.0
- sqlparse==0.5.1
- typing_extensions==4.12.2
- tzdata==2024.1
- urllib3==2.2.2
- whitenoise==6.7.0


Configuracion del proyecto
==========================
Se elege el Sistema Gestor de Base de Datos y se procede a la creacion de las correspondientes tablas,
y realizar las configuraciones. Se configura el archivo `settings.py`

En ``settings.py``:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cms',  # Nombre de la base de datos
        'USER': 'nombreUsuario',  # Nombre de usuario en el Sistema Gestor
        'PASSWORD': 'constrasenaUsuario',  # Contraseña
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

**Observacion**: tanto el nombre de usuario como la contraseña puede ser colocados en un archivo .env de manera a que no sean visibles

Pasos para ejecutar el proyecto
===============================

``Desde el directorio principal o raiz ejecutamos los siguientes comandos``

- py manage.py makemigrations
- py manage.py migrate
- py manage.py runserver
Estos comandos nos ayudan a visualizar el proyecto localmente, es decir, desde el localhost.


``Las pruebas unitarias se pueden realizar desde el directorio raiz del proyecto cms a través del siguiente comando``

- py manage.py test


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/articulos
   modules/cuentas
   modules/cms