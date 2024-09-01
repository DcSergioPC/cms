from django.urls import path
from . import views
app_name = 'articulos'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('edit/<int:article_id>', views.edit, name='edit'),
    path('delete/<int:article_id>', views.delete, name='delete'),
    ####PLANTILLAS
    path('plantilla', views.plantilla_index, name='plantilla_index'),
    path('plantilla_create', views.plantilla_create, name='plantilla_create'),
    path('plantilla_detail/<int:plantillas_id>', views.plantilla_detail, name='plantilla_detail'),
    path('plantilla_edit/<int:plantillas_id>', views.plantilla_edit, name='plantilla_edit'),
    path('plantilla_delete/<int:plantillas_id>', views.plantilla_delete, name='plantilla_delete'),
    
]