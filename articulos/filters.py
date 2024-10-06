import django_filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'author': ['exact'],  # Filtrar por autor exacto
            'categoria': ['exact'],  # Filtrar por categoría exacta
            'status': ['exact'],  # Filtrar por estado exacto
            'created_at': ['exact', 'year__gte', 'year__lte'],  # Filtrar por fecha de creación
        }
