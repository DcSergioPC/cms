from django.test import TestCase, Client
from django.urls import reverse
from categorias.models import Categoria
import json


"""class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria_list_url = reverse('categoria_list')
        self.categoria_create_url = reverse('categoria_create')
        self.categoria_update_url = reverse('categoria_update', args=[1])
        self.categoria_delete_url = reverse('categoria_delete', args=[1])
        self.categoria = Categoria.objects.create(titulo='Categoria1')

    def test_categoria_list_GET(self):
        response = self.client.get(self.categoria_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/categoria_list.html')

    def test_categoria_create_POST(self):
        response = self.client.post(self.categoria_create_url, {
            'titulo': 'Categoria2'
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(titulo='Categoria2').exists())

    def test_categoria_update_POST(self):
        response = self.client.post(self.categoria_update_url, {
            'titulo': 'Categoria1 Actualizada'
        })
        self.assertEquals(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertEquals(self.categoria.titulo, 'Categoria1 Actualizada')

    def test_categoria_delete_POST(self):
        response = self.client.post(self.categoria_delete_url)
        self.assertEquals(response.status_code, 302) 
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())
"""
from django.test import TestCase, Client
from django.urls import reverse
from categorias.models import Categoria

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria_list_url = reverse('categoria_list')
        self.categoria_create_url = reverse('categoria_create')
        self.categoria = Categoria.objects.create(titulo='Categoria1')
        self.categoria_update_url = reverse('categoria_update', args=[self.categoria.id])
        self.categoria_delete_url = reverse('categoria_delete', args=[self.categoria.id])

    def test_categoria_list_GET(self):
        response = self.client.get(self.categoria_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/categoria_list.html')

    def test_categoria_create_POST(self):
        response = self.client.post(self.categoria_create_url, {
            'titulo': 'Categoria2'
        })
        self.assertEquals(response.status_code, 302)  
        self.assertTrue(Categoria.objects.filter(titulo='Categoria2').exists())

    def test_categoria_update_POST(self):
        response = self.client.post(self.categoria_update_url, {
            'titulo': 'Categoria1 Actualizada'
        })
        self.assertEquals(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertEquals(self.categoria.titulo, 'Categoria1 Actualizada')

    def test_categoria_delete_POST(self):
        response = self.client.post(self.categoria_delete_url)
        self.assertEquals(response.status_code, 302)  
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())
