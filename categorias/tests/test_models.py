from django.test import TestCase
from categorias.models import Categoria

class TestModels(TestCase):
    
    def setUp(self):
        self.categoria1 = Categoria.objects.create(
            titulo = 'Categoria 1',
        )

class TestModels(TestCase):
    def setUp(self):
        self.categoria1 = Categoria.objects.create(
            titulo='Test de Categoria'
        )

    def test_categoria_creation(self):
        self.assertEqual(self.categoria1.titulo, 'Test de Categoria')
