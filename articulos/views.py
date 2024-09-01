from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Plantilla
from .forms import ArticleForm, PlantillaForm


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

############################### PLANTILLAS #######################
def plantilla_index(request):
    plantillas = Plantilla.objects.all()
    params = {
        'plantillas': plantillas,
    }
    return render(request, 'articulos/plantilla_index.html', params)

#CREA PLANTILLA

def plantilla_create(request):
    if request.method == 'POST':
        form = PlantillaForm(request.POST)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            # Crear una nueva instancia de Plantilla con los datos del formulario
            plantillas = Plantilla(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                contenido=form.cleaned_data['contenido']
            )
            plantillas.save()
            return redirect('articulos:plantilla_index')
    else:
        form = PlantillaForm()
    
    return render(request, 'articulos/plantilla_create.html', {'form': form})

def plantilla_detail(request, plantillas_id):
    plantillas = Plantilla.objects.get(id=plantillas_id)
    params = {
        'plantillas': plantillas,
    }
    return render(request, 'articulos/plantilla_detail.html', params)


def plantilla_edit(request, plantillas_id):
    plantilla = get_object_or_404(Plantilla, id=plantillas_id)
    
    if request.method == 'POST':
        form = PlantillaForm(request.POST, instance=plantilla) 
        if form.is_valid():
            form.save()
            return redirect('articulos:plantilla_detail', plantillas_id)
    else:
        form = PlantillaForm(instance=plantilla)  # Usa la instancia para prellenar el formulario
    
    return render(request, 'articulos/plantilla_edit.html', {'plantilla': plantilla, 'form': form})


def plantilla_delete(request, plantillas_id):
    plantilla = Plantilla.objects.get(id=plantillas_id)
    if (request.method == 'POST'):
        plantilla.delete()
        return redirect('articulos:plantilla_index')
    else:
        params = {
            'plantilla': plantilla,
        }
        return render(request, 'articulos/plantilla_delete.html', params)
        
