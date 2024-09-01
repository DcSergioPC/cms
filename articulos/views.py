from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Article
from .forms import ArticleForm


def index(request):
    articles = Article.objects.all()
    params = {
        'articles': articles,
    }
    return render(request, 'articulos/index.html', params)


"""def create(request):
    if (request.method == 'POST'):
        title = request.POST['title']
        content = request.POST['content']
        article = Article(title=title, content=content)
        article.save()
        return redirect('articulos:index')
    else:
        params = {
            'form': ArticleForm(),
        }
        return render(request, 'articulos/create.html', params)
"""
"""
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            # Crear una nueva instancia de Article con los datos del formulario
            article = Article(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                image=form.cleaned_data['image'],
                video=form.cleaned_data['video']
            )
            article.save()
            return redirect('articulos:index')
    else:
        form = ArticleForm()
    
    return render(request, 'articulos/create.html', {'form': form})"""


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
            return redirect('articulos:index')  
    else:
        form = ArticleForm()

    return render(request, 'articulos/create.html', {'form': form})


def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    params = {
        'article': article,
    }
    return render(request, 'articulos/detail.html', params)

"""
def edit(request, article_id):
    article = Article.objects.get(id=article_id)
    if (request.method == 'POST'):
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('articulos:detail', article_id)
    else:
        form = ArticleForm(initial={
            'title': article.title,
            'content': article.content,
        })
        params = {
            'article': article,
            'form': form,
        }
        return render(request, 'articulos/edit.html', params)
"""
"""
def edit(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articulos:detail', article_id)
    else:
        form = ArticleForm(initial={
            'title': article.title,
            'content': article.content,
            'image': article.image,
            'video': article.video
        })

    return render(request, 'articulos/edit.html', {'article': article, 'form': form})
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm

def edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Usa request.FILES para archivos
        if form.is_valid():
            form.save()
            return redirect('articulos:detail', article_id)
    else:
        form = ArticleForm(instance=article)  # Usa la instancia para prellenar el formulario
    
    return render(request, 'articulos/edit.html', {'article': article, 'form': form})



def delete(request, article_id):
    article = Article.objects.get(id=article_id)
    if (request.method == 'POST'):
        article.delete()
        return redirect('articulos:index')
    else:
        params = {
            'article': article,
        }
        return render(request, 'articulos/delete.html', params)

