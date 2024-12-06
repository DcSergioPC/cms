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
from articulos.models import Categoria, Article, Notification, Plantilla, ArticleVersion
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from datetime import datetime

#<<<<<  PRUEBA PARA MODELO Article >>>>>>
class ArticleModelTest(TestCase):
    
    def setUp(self):
        
        self.user = get_user_model().objects.create_user(username='usuarioprueba', password='passwordprueba') #Se crea un usuario de prueba
        self.categoria = Categoria.objects.create(titulo='Categoría Test')  #se crea categoria de prueba
        self.plantilla = Plantilla.objects.create(titulo='Plantilla Test') #se crea plantilla de prueba

    def test_create_article(self):
        article = Article.objects.create(       #se crea artículo de prueba
            title="Test Article",
            content="Esta es una prueba de modelo de Articulo",
            author=self.user,
            categoria=self.categoria,
            plantilla=self.plantilla
        )
        
        # Se verifica que el articulo se guarde de forma correcta
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.content, "Esta es una prueba de modelo de Articulo")
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.categoria, self.categoria)
        self.assertEqual(article.plantilla, self.plantilla)
        
    def test_article_str_method(self):
        article = Article.objects.create(
            title="Test Article",
            content="Este es el contenido de test article.",
            author=self.user,
            categoria=self.categoria,
            plantilla=self.plantilla
        )
        
        
        self.assertEqual(str(article), "Test Article, Este es el contenido de test article.")
    
    def test_default_status(self):
        article = Article.objects.create(
            title="Test Article",
            content="Este es el contenido de test article.",
            author=self.user,
            categoria=self.categoria,
            plantilla=self.plantilla
        )
        
        # Debemos ver que el status es por defecto 'pendiente'
        self.assertEqual(article.status, 'pendiente')
    
    def test_article_status_choices(self):
        article = Article.objects.create(
            title="Test Article",
            content="Este es el contenido de test article.",
            author=self.user,
            categoria=self.categoria,
            plantilla=self.plantilla,
            status='publicado'
        )
        
        # Verificar que el artículo tiene el estado correcto
        self.assertEqual(article.status, 'publicado')


#<<<  PRUEBA PARA ArticleVersion >>>>

class ArticleVersionModelTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='usuarioprueba', password='passwordprueba') #se crea usuario de prueba
        self.article = Article.objects.create(  #se crea articulo de prueba
            title="Test Article",
            content="Esta es una prueba de modelo de ArticleVersion.",
            author=self.user
        )
        
    def test_create_article_version(self):
        version = ArticleVersion.objects.create(    #se crea una version para el articulo
            article=self.article,
            change_description="Primera version",
            title="Version 1 Title",
            content="Version 1 Content",
            changed_by=self.user,
            categoria="Test Categoria",
            plantilla="Test Plantilla",
            author=self.user
        )
        
        # se verfica que la version del articulo se crea de forma correcta
        self.assertEqual(version.article, self.article)
        self.assertEqual(version.change_description, "Primera version")
        self.assertEqual(version.title, "Version 1 Title")
        self.assertEqual(version.content, "Version 1 Content")
        self.assertEqual(version.changed_by, self.user)
        self.assertEqual(version.categoria, "Test Categoria")
        self.assertEqual(version.plantilla, "Test Plantilla")
    
    def test_article_version_str_method(self):
        version = ArticleVersion.objects.create(    #se crea una version del articulo
            article=self.article,
            change_description="Primera version",
            title="Version 1 Title",
            content="Version 1 Content",
            changed_by=self.user,
            categoria="Test Categoria",
            plantilla="Test Plantilla",
            author=self.user
        )
        self.assertEqual(str(version), "Version 1 Title, Version 1 Content")
    
    def test_default_categoria_and_plantilla(self):
        version = ArticleVersion.objects.create( #se crea un articulo sin categoria y plantilla
            article=self.article,
            change_description="Primera version",
            title="Version 1 Title",
            content="Version 1 Content",
            changed_by=self.user,
            author=self.user
        )
        self.assertEqual(version.categoria, "Sin Categoría") #se verifica que los valores por defecto son correctos
        self.assertEqual(version.plantilla, "Sin Plantilla")



















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

#from django.contrib.auth import get_user_model

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
        

