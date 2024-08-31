from django.db import models

# Create your models here.


class Categoria(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
