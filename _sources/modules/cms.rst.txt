CMS
===

Configuración
-------------

Configuración de Django para el proyecto cms.

Generado por ‘django-admin startproject’ usando Django 5.1.

Para obtener más información sobre este archivo, consulte https://docs.djangoproject.com/en/5.1/topics/settings/

Para obtener la lista completa de configuraciones y sus valores, consulte https://docs.djangoproject.com/en/5.1/ref/settings/

..
   .. automodule:: cms.settings
   :members:

URLs
----

Configuración de URL para el proyecto cms.

La lista urlpatterns enruta las URL a las vistas. Para obtener más información, consulte:
https://docs.djangoproject.com/en/5.1/topics/http/urls/

Ejemplos: Vistas de función

- Agregar una importación: from my_app import views

- Agregar una URL a urlpatterns: path(‘’, views.home, name=’home’)

Vistas basadas en clases

- Agregar una importación: from other_app.views import Home

- Agregar una URL a urlpatterns: path(‘’, Home.as_view(), name=’home’)

Incluir otra URLconf

- Importar la función include(): from django.urls import include, path

- Agregar una URL a urlpatterns: path(‘blog/’, include(‘blog.urls’))

..
   .. automodule:: cms.urls
   :members:
