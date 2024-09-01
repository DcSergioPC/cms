from django.test import TestCase
from django.urls import reverse, resolve
from articulos.views import index, create, detail, edit, delete
from articulos.models import Article
from django.core.files.uploadedfile import SimpleUploadedFile

class TestUrls(TestCase):
    def setUp(self):
        #se crea articulo de prueba
        self.article = Article.objects.create(
            title='Test',
            content='Test articulo.',
            image=SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg'),
            video=SimpleUploadedFile('test_video.mp4', b'file_content', content_type='video/mp4')
            
        )
    def test_index_url_is_resolves(self):
        url = reverse('articulos:index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)
        
    def test_create_url_is_resolves(self):
        url = reverse('articulos:create')
        print(resolve(url))
        self.assertEquals(resolve(url).func, create)

    def test_detail_url_is_resolves(self):
        url = reverse('articulos:detail', args=[self.article.id])
        print(resolve(url))
        self.assertEquals(resolve(url).func, detail)
        
    def test_edit_url_is_resolved(self):
        url = reverse('articulos:edit', args=[self.article.id])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit)
    
    def test_delete_url_is_resolved(self):
        url = reverse('articulos:delete', args=[self.article.id])
        print(resolve(url))
        self.assertEquals(resolve(url).func, delete)