from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('nueva/', views.categoria_create, name='categoria_create'),
    path('<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
]
