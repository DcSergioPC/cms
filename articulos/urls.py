from django.urls import path
from . import views
from .views import notifications_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
    ####CATEGORIAS
    path('categoria', views.categoria_list, name='categoria_list'),
    path('categoria_nueva', views.categoria_create, name='categoria_create'),
    path('categoria_editar/<int:pk>', views.categoria_update, name='categoria_update'),
    path('categoria_eliminar/<int:pk>', views.categoria_delete, name='categoria_delete'),
    ##Comentarios
    path('comentario/edit/<int:comentario_id>/', views.edit_comentario, name='edit_comentario'),
    path('comentario/delete/<int:comentario_id>/', views.delete_comentario, name='delete_comentario'),
    ##Manejo de Articulos
    path('tablero_kanban', views.tablero_kanban, name='tablero_kanban'),
    path('estado_publicacion', views.manejar_articulos, name='manejar_articulos'),  # Para gestionar artículos pendientes
    path('publicados', views.articulos_publicados, name='articulos_publicados'),  # Para ver publicaciones aceptadas
    path('aceptar/<int:article_id>/', views.aceptar_articulo, name='aceptar_articulo'),  # Para aceptar un artículo
    path('reject/<int:article_id>/', views.reject_article, name='reject_article'),
    ##Para ver articulo antes de publicar
    path('ver_articulo/<int:article_id>', views.ver_articulo, name='ver_articulo'),
    path('actualiza/<int:article_id>/', views.actualiza_articulo, name='actualiza_articulo'),
    path('notificaciones/', views.notifications_view, name='notifications'),
    ## Para ver estadisticas
    path('reportes', views.reportes, name='reportes'),
    ##toggle like
    path('like/<int:article_id>/', views.toggle_like, name='toggle_like'),
    path('historial/<int:article_id>', views.cambios_articulo, name='historial'),
    path('articulos/<int:article_id>/version/<int:version_id>/', views.version_detail, name='version_detail'),
]

urlpatterns += staticfiles_urlpatterns()