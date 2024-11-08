import concurrent.futures
from itertools import count
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Plantilla, Categoria, Comentario, Notification
from .forms import ArticleForm, PlantillaForm, CategoriaForm, ComentarioForm
from cms.services.email import send_confirmation_email, send_email_to_role
from cuentas.models import CustomUser
from django.core.paginator import Paginator

from .filters import ArticleFilter, PublicadoFilter  # Importamos el filtro que se creó en filters.py

from django.db.models import Count
from django.db.models.functions import TruncMonth

###############################Notificaciones
def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.filter(is_read=False).update(is_read=True)
    paginator = Paginator(notifications, 20)  #muestra hasta 20 notificaciones
    #se obtiene numero de pagina de notificaciones
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)
    
    return render(request, 'articulos/notificaciones.html', {'notifications': notifications_page})
###############################Notificaciones

def article_list(request):
    articles = Article.objects.all()
    filter = ArticleFilter(request.GET, queryset=articles)  # Aplicamos el filtro

    return render(request, 'articulos/index.html', {'filter': filter})


def index(request):
    if request.user.is_authenticated:
        articles = Article.objects.filter(author=request.user)  # Solo artículos del usuario autenticado

        # Aplicar el filtro
        article_filter = ArticleFilter(request.GET, queryset=Article.objects.all())
    
        # Obtener los artículos filtrados
        articles = article_filter.qs
        # Si inicia sesion con rol invitado le redirige a la pagina de publicaciones
        if request.user.role == 'guest':
            return render(request, 'articulos/articulos_publicados.html', {
            'filter': article_filter,
            'articles': articles,
            })
        else:    
            return render(request, 'articulos/index.html', {'filter': article_filter, 'articles': articles})
        #return render(request, 'articulos/index.html', {'articles': articles})
    return redirect('login')  # Redirige si no está autenticado

######
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  
        if form.is_valid():
            #form.save()
            article = form.save(commit=False)
            article.author = request.user  # Asigna el autor
            article.status = 'pendiente'  # Establece el estado a "pendiente"
            article.save()
            # Enviar correo al usuario que creó el artículo
            first_name = request.user.first_name or ''
            last_name = request.user.last_name or ''
            
            #notificación para administradores y editores
            for user in CustomUser.objects.filter(role__in=['admin', 'editor']).exclude(pk=request.user.pk):
                create_notification(user, f'Se ha creado un nuevo artículo: {article.title}')
            
            # Ejecutar métodos de envío de correo de manera asíncrona
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Enviar correo al creador del artículo
                send_confirmation_email(request.user, article, action='create')
                # Enviar correo a los del mismo rol, excluyendo al creador
                send_email_to_role(article, request.user, action='create', roles=['admin','editor'])

            return redirect('articulos:index')
    else:
        form = ArticleForm()

    return render(request, 'articulos/create.html', {'form': form})
'''
def manejar_articulos(request):
    articles = Article.objects.filter(status='pending')
    return render(request, 'articulos/manejar_articulos.html', {'articles': articles})
'''
def aceptar_articulo(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.status = 'aprobado'
    article.save()
    
    #notificación sobre el cambio de estado
    create_notification(article.author, f"Tu artículo '{article.title}' ha sido aprobado.")
    
    return redirect('articulos:manejar_articulos')


def reject_article(request, article_id):
    article = Article.objects.get(id=article_id)
    article.status = 'rechazado'
    article.save()
    
    
    #notificación sobre el cambio de estado
    create_notification(article.author, f"Tu artículo '{article.title}' ha sido rechazado.")
    
    return redirect('articulos:manejar_articulos')

def publicar_articulo(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user.role == 'admin': 
        article.status = 'publicado'
        article.save()
    
    #notificación sobre el cambio de estado
    create_notification(article.author, f"Tu artículo '{article.title}' ha sido publicado.")
    
    return redirect('articulos:manejar_articulos')

def articulos_publicados(request):
    articles = Article.objects.filter(status='publicado')
    # Aplicar el filtro
    article_filter = PublicadoFilter(request.GET, queryset=articles)
    
    # Obtener artículos filtrados
    articles = article_filter.qs
    
    #contador de notificaciones no leídas
    unread_notifications_count = request.user.notification_set.filter(is_read=False).count() if request.user.is_authenticated else 0
    
    return render(request, 'articulos/articulos_publicados.html', {
        'filter': article_filter,
        'articles': articles,
        'unread_notifications_count': unread_notifications_count,
    })

def manejar_articulos(request):
    #comprobamos si el usuario es el administrador
    if request.user.is_authenticated: 
        articles = Article.objects.filter(status__in=['pendiente', 'revision', 'aprobado'])
        return render(request, 'articulos/manejar_articulos.html', {'articles': articles})
    return redirect('articulos:index')  

def ver_articulo(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    # if article.status in ['pendiente', 'revision']:
    #     article.status = 'revision'
    #     article.save()
    
    if request.method == 'POST':
        if 'aceptar' in request.POST:
            article.status = 'revision'
            article.save()
        elif 'rechazar' in request.POST:
            article.status = 'pendiente'
            article.save()
        elif 'aprobar' in request.POST:
            article.status = 'aprobado'
            article.save()
        elif 'publicar' in request.POST and request.user.role == 'admin':   
            article.status = 'publicado'
            article.save()
    
    return render(request, 'articulos/ver_articulo.html', {'article': article, 'myRole': request.user.role})

def actualiza_articulo(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        previous_status = article.status
        if 'aceptar' in request.POST:
            article.status = 'revision'
            article.save()
        elif 'rechazar' in request.POST:
            article.status = 'rechazado'
            article.save()
        elif 'aprobar' in request.POST:
            article.status = 'aprobado'
            article.save()
        elif 'publicar' in request.POST:   
            article.status = 'publicado'
            article.save()
        if(previous_status != article.status):
            # Ejecutar métodos de envío de correo de manera asíncrona
            with concurrent.futures.ThreadPoolExecutor() as executor:
                send_confirmation_email(request.user, article, action='update')
                send_email_to_role(article, request.user, action='update', roles=['admin','editor'])
    return redirect('articulos:tablero_kanban')



def tablero_kanban(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()  # Solo artículos del usuario autenticado
        unread_notifications_count = request.user.notification_set.filter(is_read=False).count()  # Contar notificaciones no leídas
        
        return render(request, 'articulos/kanban.html', {
            'articles': articles,
            'unread_notifications_count': unread_notifications_count,  # Pasar el conteo al contexto
        })
    return redirect('login')  # Redirige si no está autenticado




######
'''def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    params = {
        'article': article,
    }
    return render(request, 'articulos/detail.html', params)
'''


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comentarios = article.comentarios.all()
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.article = article
            comentario.user = request.user
            comentario.save()
            return redirect('articulos:detail', article_id=article.id)
    else:
        form = ComentarioForm()

    params = {
        'article': article,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'articulos/detail.html', params)

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
        

############################### CATEGORIAS #######################

def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'articulos/categoria_list.html', {'categorias': categorias})

def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articulos:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'articulos/categoria_form.html', {'form': form})

def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('articulos:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'articulos/categoria_form.html', {'form': form})

def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('articulos:categoria_list')
    return render(request, 'articulos/categoria_confirm_delete.html', {'categoria': categoria})


def edit_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifica que el usuario sea el autor del comentario
    if comentario.user != request.user:
        return redirect('articulos:detail', article_id=comentario.article.id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('articulos:detail', article_id=comentario.article.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'articulos/edit_comentario.html', {
        'form': form,
        'article': comentario.article,  
    })

def delete_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifica que el usuario sea el autor del comentario
    if comentario.user == request.user:
        comentario.delete()
    
    return redirect('articulos:detail', article_id=comentario.article.id)


# vistas de reportes
def reportes(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()
        unread_notifications_count = request.user.notification_set.filter(is_read=False).count()
        
        # Obtener la cantidad de artículos publicados por cada usuario con el estado "publicado"
        articles_by_user = Article.objects.filter(status='publicado').values('author__username').annotate(count=Count('id'))
        # Obtener la cantidad de artículos publicados por mes
        articles_by_month = Article.objects.filter(status='publicado').annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')


        return render(request, 'articulos/reportes.html', {
            'articles': articles,
            'unread_notifications_count': unread_notifications_count,
            'articles_by_user': articles_by_user,  # Pasar los datos al contexto
            'articles_by_month': articles_by_month,  # Pasar los datos al contexto
        })
    return redirect('login')

