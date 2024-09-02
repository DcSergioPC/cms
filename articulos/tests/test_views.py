"""
from django.test import TestCase, Client
from django.urls import reverse
from articulos.models import Article
import json
from django.core.files.uploadedfile import SimpleUploadedFile
#index, create, detail, edit, delete

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('articulos:index')
        self.create_url = reverse('articulos:create')
        self.detail_url = reverse('articulos:detail')
        self.article = Article.objects.create(
            title='Test',
            content='test articulo.',
            image=SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg'),
            video=SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4')
        )
        self.detail_url = reverse('articulos:detail', args=[self.article.id])
        self.edit_url = reverse('articulos:edit', args=[self.article.id])
        self.delete_url = reverse('articulos:delete', args=[self.article.id])
        
    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/index.html')
        
    def test_create_GET(self):
        response = self.client.get(self.create_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/create.html')
        
    def test_detail_GET(self):
        response = self.client.get(self.detail_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/detail.html')
"""
"""
from django.test import TestCase, Client
from django.urls import reverse
from articulos.models import Article
from categorias.models import Categoria
from django.core.files.uploadedfile import SimpleUploadedFile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('articulos:index')
        self.create_url = reverse('articulos:create')

        # Crear una categoría de prueba
        self.categoria = Categoria.objects.create(titulo='Test Category')

        # Crear un artículo de prueba para usar en otras pruebas
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article.',
            image=SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg'),
            video=SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4'),
            categoria=self.categoria  # Asociar la categoría al artículo
        )
        self.detail_url = reverse('articulos:detail', args=[self.article.id])
        self.edit_url = reverse('articulos:edit', args=[self.article.id])
        self.delete_url = reverse('articulos:delete', args=[self.article.id])

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/index.html')

    def test_create_GET(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/create.html')
        
    def test_create_POST(self):
        response = self.client.post(self.create_url, {
            'title': 'New Article',
            'content': 'Content for new article.',
            'image': SimpleUploadedFile('new_image.jpg', b'file_content', content_type='image/jpeg'),
            'video': SimpleUploadedFile('new_video.mp4', b'file_content', content_type='video/mp4'),
            'categoria': self.categoria.id  # Asegúrate de incluir la categoría
        })
        self.assertEquals(response.status_code, 302)  
        self.assertRedirects(response, self.index_url)
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/detail.html')
        
    def test_edit_GET(self):
        response = self.client.get(self.edit_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos/edit.html')

    def test_edit_POST(self):
        response = self.client.post(self.edit_url, {
            'title': 'Updated Article',
            'content': 'Updated content.',
            'image': SimpleUploadedFile('updated_image.jpg', b'file_content', content_type='image/jpeg'),
            'video': SimpleUploadedFile('updated_video.mp4', b'file_content', content_type='video/mp4'),
            'categoria': self.categoria.id  # Asegúrate de incluir la categoría
        })
        self.assertEquals(response.status_code, 302)  
        self.assertRedirects(response, self.detail_url)
        self.article.refresh_from_db()
        self.assertEquals(self.article.title, 'Updated Article')

    def test_delete_POST(self):
        response = self.client.post(self.delete_url)
        self.assertEquals(response.status_code, 302)  
        self.assertRedirects(response, self.index_url)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())
"""

""" from django.test import TestCase, Client
from django.urls import reverse
from categorias.models import Categoria
import json """


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
""" from django.test import TestCase, Client
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
 """
 