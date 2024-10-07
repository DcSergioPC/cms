from django.db import models
#from .models import Categoria

from django.conf import settings


##TABLA CATEGORIAS
class Categoria(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
    
class Plantilla(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    contenido = models.TextField()
    
    def __str__(self):
        return f'{self.titulo}, {self.descripcion}, {self.contenido}'
    
# Se actualizo para agregar estado
class Article(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('revision', 'Revision'),
        ('aprobado', 'Aprobado'),
        ('publicado', 'Publicado'),
        ('rechazado', 'Rechazado'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()

    ##################
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    ####################
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Usuario que creó el artículo
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title}, {self.content}'
    

##




class Comentario(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegúrate de usar esto
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.article.title}'



