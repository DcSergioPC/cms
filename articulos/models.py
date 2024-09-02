from django.db import models
#from .models import Categoria


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
    
# Create your models here.
class Article(models.Model):
    
    title = models.CharField(max_length=255)
    content = models.TextField()

    ##################
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    ####################
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}, {self.content}'
    