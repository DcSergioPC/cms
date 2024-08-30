from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    ##################
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    ####################
    
    def __str__(self):
        return f'{self.title}, {self.content}'