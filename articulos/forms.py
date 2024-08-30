"""
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    content = forms.CharField(label='Content', widget=forms.Textarea())
    image = forms.ImageField(label='Image', required=False)  # Campo para imagen
    video = forms.FileField(label='Video', required=False)   # Campo para video
"""
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }