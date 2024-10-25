""" from django.test import TestCase
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
 """
 
from django.test import TestCase
from articulos.models import Categoria, Article, Notification

class TestModels(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            titulo='Test Categoria'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article.',
            image='test_image.jpg', 
            video='test_video.mp4', 
            categoria=self.categoria
        )

    def test_categoria_creation(self):
        self.assertEqual(self.categoria.titulo, 'Test Categoria')

    def test_article_creation(self):
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.categoria, self.categoria)

from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_notification_creation(self):
        notification = Notification.objects.create(user=self.user, message='Test notification')
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, 'Test notification')
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)