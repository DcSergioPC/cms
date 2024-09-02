"""
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    content = forms.CharField(label='Content', widget=forms.Textarea())
    image = forms.ImageField(label='Image', required=False)  # Campo para imagen
    video = forms.FileField(label='Video', required=False)   # Campo para video
"""
from django import forms
from .models import Article, Plantilla, Categoria
##from categorias.models import Categoria

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'video','categoria']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].required = True

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['titulo', 'descripcion', 'contenido']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']