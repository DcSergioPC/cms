from django.test import TestCase
from django.urls import reverse, resolve
from categorias.views import categoria_list, categoria_create, categoria_update, categoria_delete
from categorias.models import Categoria

class TestUrls(TestCase):
    def setUp(self):
        # Crear una categoría de prueba
        self.category = Categoria.objects.create(titulo='Test Categoria')
        self.category_id = self.category.pk
    
    def test_categoria_list_url_is_resolves(self):
        url = reverse('categoria_list')
        self.assertEqual(url, '/categorias/')

    def test_categoria_create_url_is_resolves(self):
        url = reverse('categoria_create')
        self.assertEqual(url, '/categorias/nueva/')

    def test_categoria_update_url_is_resolves(self):
        url = reverse('categoria_update', kwargs={'pk': self.category_id})
        self.assertEqual(url, f'/categorias/{self.category_id}/editar/')

    def test_categoria_delete_url_is_resolves(self):
        url = reverse('categoria_delete', kwargs={'pk': self.category_id})
        self.assertEqual(url, f'/categorias/{self.category_id}/eliminar/')








