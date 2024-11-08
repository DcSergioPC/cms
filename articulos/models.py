from django.db import models
#from .models import Categoria

from django.conf import settings

###############################Notificaciones
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
################################



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
    
class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegúrate de usar esto
    created_at = models.DateTimeField(auto_now_add=True)

    def toggle_like(article, user):
        like = Like.objects.filter(article=article, user=user).first()
        if like:
            like.delete()
        else:
            like = Like.objects.create(article=article, user=user)
        return like
    
    def filterArticleLikedByUser(articles, user):
        articles_ids = [article.id for article in articles]
        likes = Like.objects.filter(article_id__in=articles_ids, user=user)
        liked_articles_ids = [like.article.id for like in likes]
        for article in articles:
            article.liked = article.id in liked_articles_ids
        return articles
    
    def ifArticleLikedByUser(article, user):
        like = Like.objects.filter(article=article, user=user).first()
        return like is not None

    def __str__(self):
        return f'Like de {self.user.username} en {self.article.title}'
    
class View(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegúrate de usar esto
    created_at = models.DateTimeField(auto_now_add=True)
    def create_View_If_Not_Exists(article, user):
        view = View.objects.filter(article=article, user=user).first()
        if not view:
            view = View.objects.create(article=article, user=user)
        return view

    def __str__(self):
        return f'Vista de {self.user.username} en {self.article.title}'
    

##




class Comentario(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegúrate de usar esto
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.article.title}'



