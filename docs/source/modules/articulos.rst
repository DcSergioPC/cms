Artículos
=========

Modelos
-------

**Descripción de Clases de models.py**

- Categoria

.. code-block:: python

    class Categoria(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

importamos el modulo models para definir los modelos en nuestro proyecto CMS

Para representar la estructura de Categorias se utiliza una clase Categoria que posee un campo que almacena el nombre de dicha categoria. En este caso se utiliza CharField para definir una tamano maximo para el texto 


- Plantilla

.. code-block:: python

    class Plantilla(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    contenido = models.TextField()
    
    def __str__(self):
        return f'{self.titulo}, {self.descripcion}, {self.contenido}'

Para representar la estructura de Plantillas utilizamos una clase llamada Plantilla 

El atributo titulo sera el nombre de la plantilla. Tendra un tamano maximo de 255 caracteres utilizando CharField

El atributo descripcion almacena la descripcion de la Plantilla. En este caso, mediante TextField

El atributo contenido almacena el contenido de la plantilla que se define en la seccion de plantillas del proyecto cms

- Article

.. code-block:: python

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

Modelo Article representa la estructura de un articulo en la base de datos

El atributo titulo sera el nombre del articulo. Tendra un tamano maximo de 255 caracteres utilizando CharField

El atributo content almacena el contenido del articulo que se define en la seccion de articulos del proyecto cms

El atributo image permite subir imagenes para los articulos utilizando ImageField (blank=True y null=True indica que es opcional)

El atributo video permite subir videos para los articulos utilizando FileField (blank=True y null=True indica que es opcional)

El atributo categoria es un campo de clave foranea que relaciona el articulo con una categoria Categoria existente. En el caso de que se elimina la categoria, el articulo no se eliminara debido a on_delete=models.SET_NULL, que pondra al campo categoria en NULL

El atributo plantilla es un campo de clave foranea que relaciona el articulo con una plantilla Plantilla existente. En el caso de que se elimina la Plantilla, el articulo no se eliminara debido a on_delete=models.SET_NULL, que pondra al campo Plantilla en NULL

- Comentario

.. code-block:: python

    class Comentario(models.Model):
        article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comentarios')
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegúrate de usar esto
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.article.title}'

Se utiliza modelo de Comentario. Con este modelo se crea una base de datos para comentarios

Mediante el campo article se crea una relacion de clave foranea con modelo Article. Con esto, el objetivo es asociar cada comentario con articulos dependiendo de la clave

Mediante el campo user se crea una relacion de clave foranea con modelo Article. Con esto, se asocia cada el usuario con el modelo de usuario

En el campo content se guarda el contenido del comentario que realiza el usuario

Cuando el usuario realiza comentarios, éste almacena la fecha en el campo created_at (fecha y hora)

- Notification

.. code-block:: python
    
    ###############################Notificaciones
    class Notification(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        message = models.TextField()
        is_read = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.user.username} - {self.message[:20]}"

Se utiliza modelo de Notification para representar notificaciones del sistema CMS

En el campo user se establece una relacion que permita que un usuario pueda recibir una o mas notificaciones

El modelo de usuario que se utiliza esta representado por settings.AUTH_USER_MODEL (personalizado)

El campo message almacena texto que representa el mensaje de la notificacion

El campo is_read por defecto esta en false, indica si la notificacion se ha leido o no

El campo created_at refleja la hora y fecha con DateTimeField automaticamente

- Like

.. code-block:: python

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

Se utiliza modelo de Like para que el usuario con un rol determinado pueda dar "Me gusta" a la publicación

Se utiliza el campo article para asociar el modelo Like con Article para representar la relacion entre el articulo y el "Me gusta" del usuario y mediante on_delete=models.CASCADE se especifica que se borraran los registros de me gusta si se elimina la publicacion

Se utiliza el campo user para especificar el usuario. En este caso el usuario es personalizado (en models - CustomUser) por lo que se utiliza settings.AUTH_USER_MODEL

Se utiliza el campo created_At para definir la fecha.

El método toggle_like permite hacer y deshacer el "Me gusta"

El método filterArticleLikedByUser muestra los articulos que han sido del agrado del usuario. Es decir, aquellos que recibieron "Me gusta"

El método ifArticleLikedByUser establece si el usuario ha dado o no "Me gusta" a la publicacion por medio de valores booleanos True o False (atributo)

- View

.. code-block:: python

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
    
Se utiliza modelo de View que permite registrar las vistas de las publicaciones

Se utiliza el campo article para asociar el modelo View con Article para representar la relacion entre el articulo y la vista del usuario y mediante on_delete=models.CASCADE se especifica que se borraran los registros de vistas (todos los asociados a un articulo) si se elimina la publicacion

Se utiliza el campo user para especificar el usuario. En este caso el usuario es personalizado (en models - CustomUser) por lo que se utiliza settings.AUTH_USER_MODEL

Se utiliza el campo created_At para definir la fecha.

El método create_View_If_Not_Exists permite registrar la visualizacion del usuario solo una vez (no cuenta una vista por cada vez que el usuario accede)

Solo en el caso de que el usuario no haya visto el articulo, se crea la vista con view = View.objects.create(article=article, user=user)

- ArticleVersion

.. code-block:: python
    
    class ArticleVersion(models.Model):
    
    change_description = models.TextField()
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='histories')
    change_date = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='article_changes')
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    ##################
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    ####################
    categoria = models.CharField(max_length=100, default='Sin Categoría')  # Agrega un valor por defecto
    plantilla = models.TextField(default='Sin Plantilla')    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Usuario que creó el artículo
    
    def __str__(self):
        return f'{self.title}, {self.content}'

En el campo change_description se detalla a través de una descripción que cambios se realizan en articulo

En el campo article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='histories') se relaciona al modelo Article para establecer a qué artículo hacemos referencia. Con (on_delete = models.CASCADE) desaparecen las versiones en caso de eliminacióno

En el campo change_date se guarda la fecha y hora de creación de versión

En el campo changed_by se guarda quién realizó los cambios para esa versión 

El campo title almacena el título del articulo

El campo content almacena el contenido del articulo

El campo image almacena la imagen del articulo

El campo video almacena el video del articulo

El campo categoria almacena la categoría del articulo

El campo plantilla almacena la plantilla del articulo

El campo author almacena el autor del articulo

=======================================
Documentacion generada por Sphinx 8.0.2
=======================================

..
   .. automodule:: articulos.models
   :members:
   :undoc-members:
   :show-inheritance:

Vistas
------

**Descripción de Clases de views.py**

- index

.. code-block:: python

      def index(request):
    if request.user.is_authenticated:
        articles = Article.objects.filter(author=request.user)  # Solo artículos del usuario autenticado

        # Aplicar el filtro
        article_filter = ArticleFilter(request.GET, queryset=Article.objects.all())
    
        # Obtener los artículos filtrados
        articles = article_filter.qs


        return render(request, 'articulos/index.html', {'filter': article_filter, 'articles': articles})
        #return render(request, 'articulos/index.html', {'articles': articles})
    return redirect('login')

Se obtiene todos los registros de tabla Article que esta almacenada en la base de datos

Se guardan los articulos en diccionario params, donde la clave es 'articles' y el valor es el definido arriba (articles)

Se visualiza la lista de articulos mediante render(request, 'articulos/index.html', params) que renderiza la plantilla pasandole los datos del diccionario

- create

.. code-block:: python

   def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  
        if form.is_valid():
            #form.save()
            article = form.save(commit=False)
            article.author = request.user  # Asigna el autor
            article.status = 'pendiente'  # Establece el estado a "pending"
            article.save()  
            return redirect('articulos:index')  
    else:
        form = ArticleForm()

    return render(request, 'articulos/create.html', {'form': form})

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con ArticleForm(request.POST, request.FILES) se crea un objeto formulario con los datos ingresdos por el usuario

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

- detail

.. code-block:: python

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

detail muestra los detalles de un articulo

Se obtiene el articulo con el ID correspondiente mediante Article.objects.get(id=article_id)

Se guardan los articulos en diccionario params, donde la clave es 'articles' y el valor es el definido arriba (articles)

Se visualizan articulos mediante render(request, 'articulos/index.html', params) que renderiza la plantilla detail.html pasandole los datos del diccionario

- edit 

.. code-block:: python

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

Se obtiene el articulo con el ID correspondiente mediante get_object_or_404(Article, id=article_id). Si no existe, error 404

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con ArticleForm(request.POST, request.FILES, instance=article) se cargan objeto formulario con los datos ingresados por el usuario en el articulo

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

- delete

.. code-block:: python

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

Mediante Article.objects.get(id=article_id) obtenemos el articulo a eliminar

Se usa la condicional if request.method == 'POST' que define que el usuario quiere eliminar el articulo

El articulo se elimina de la base de datos con article.delete()

En el caso de que sea un metodo GET, el sistema muestra una pantalla para confirmar eliminacion

- plantilla_index

.. code-block:: python

   def plantilla_index(request):
    plantillas = Plantilla.objects.all()
    params = {
        'plantillas': plantillas,
    }
    return render(request, 'articulos/plantilla_index.html', params)

Se obtiene todas las plantillas almacenadas en la base de datos mediante Plantilla.objects.all()

Mediante el uso de diccionario params, las plantillas se guardan con clave "plantillas" y valor "plantillas"

Utilizando render(request, 'articulos/plantilla_index.html', params) se renderiza la plantilla plantilla_index.html, en donde se muestran en la pagina de lista de plantillas las plantillas almacenadas

- plantilla_create

.. code-block:: python

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

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con PlantillaForm(request.POST) se crea un formulario con datos de plantilla del usuario 

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

Se renderiza la plantilla plantilla_create.html pasando el formulario con render(request, 'articulos/plantilla_create.html', {'form': form}).

- plantilla_detail

.. code-block:: python

   def plantilla_detail(request, plantillas_id):
    plantillas = Plantilla.objects.get(id=plantillas_id)
    params = {
        'plantillas': plantillas,
    }
    return render(request, 'articulos/plantilla_detail.html', params)

Se obtiene la plantilla con el ID que se especifica en Plantilla.objects.get(id=plantillas_id) mediante una consulta a la base de Datos

Mediante el uso de diccionario params, las plantillas se guardan con clave "plantillas" y valor "plantillas"

Se renderiza la plantilla plantilla_detail.html pasando el formulario con render(request, 'articulos/plantilla_create.html', {'form': form}).

- plantilla_edit

.. code-block:: python

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

Se obtiene la plantilla con el ID correspondiente mediante get_object_or_404(Plantilla, id=plantillas_id). Si no existe, error 404

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con PlantillaForm(request.POST, instance=plantilla) se cargan objeto formulario con los datos ingresados por el usuario en la plantilla

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

- plantilla_delete

.. code-block:: python

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

Se obtiene la plantilla con el ID que se especifica en Plantilla.objects.get(id=plantillas_id) mediante una consulta a la base de Datos

Se usa la condicional if request.method == 'POST' que define que el usuario quiere eliminar la plantilla

La plantilla se elimina de la base de datos con plantilla.delete()

En el caso de que sea un metodo GET, el sistema muestra una pantalla para confirmar eliminacion

- categoria_list

.. code-block:: python

   def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'articulos/categoria_list.html', {'categorias': categorias})

Se obtiene las categorias con Categoria.objects.all() mediante una consulta a la base de Datos

Se renderiza la plantilla categoria_list.html, en donde render(request, 'articulos/categoria_list.html', {'categorias': categorias}) pasa las categorias para visualizar en la pagina de categorias

- categoria_create

.. code-block:: python

   def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articulos:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'articulos/categoria_form.html', {'form': form})

Su funcion es crear una nueva categoria

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

- categoria_update

.. code-block:: python

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

Se obtiene la categoria con el ID que se especifica en get_object_or_404(Categoria, pk=pk) mediante una consulta a la base de Datos

Se usa la condicional if request.method == 'POST' que define que el usuario envia un formulario

Con form.is_valid() se validan los datos del formulario y se guardan con form.save()

- categoria_delete

.. code-block:: python

   def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('articulos:categoria_list')
    return render(request, 'articulos/categoria_confirm_delete.html', {'categoria': categoria})

Se obtiene la categoria con el ID que se especifica en get_object_or_404(Categoria, pk=pk) mediante una consulta a la base de Datos

Se usa la condicional if request.method == 'POST' que define que el usuario quiere eliminar la categoria

La categoria se elimina de la base de datos con categoria.delete()

- article_list

.. code-block:: python

    def article_list(request):
        articles = Article.objects.all()
        filter = ArticleFilter(request.GET, queryset=articles)  # Aplicamos el filtro

    return render(request, 'articulos/index.html', {'filter': filter})

Se obtiene todos los objetos del modelo Article que estan almancenados en la base de datos con Article.objects.all()

Con Django Filter se utliza un filtro para filtrar articulos dependiendo de los requerimientos, como categorias, plantillas, etc. Los parametros de la solicitud GET son pasados al filtro



- aceptar_articulo

.. code-block:: python

    def aceptar_articulo(request, article_id):
        article = get_object_or_404(Article, id=article_id)
        article.status = 'aprobado'
        article.save()
        return redirect('articulos:manejar_articulos')

Se obtiene el articulo con el ID correspondiente mediante get_object_or_404(Article, id=article_id). Si no existe, error 404

Se asigna el estado "aprobado" al articulo con article.status = 'aprobado', luego se guarda con article.save()



- reject_article

.. code-block:: python

    def reject_article(request, article_id):
        article = Article.objects.get(id=article_id)
        article.status = 'rechazado'
        article.save()
        return redirect('articulos:manejar_articulos')

Se obtiene el articulo con el ID correspondiente mediante get_object_or_404(Article, id=article_id). Si no existe, error 404

Se asigna el estado "rechazado" al articulo con article.status = 'rechazado', luego se guarda con article.save()

- publicar_articulo

.. code-block:: python

    def publicar_articulo(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user.role == 'admin': 
        article.status = 'publicado'
        article.save()
    return redirect('articulos:manejar_articulos')

Se obtiene el articulo con el ID correspondiente mediante get_object_or_404(Article, id=article_id). Si no existe, error 404

Si el rol de usuario es "admin" se asigna el estado "publicado" al articulo con article.status = 'publicado', luego se guarda con article.save()

- articulos_publicados

.. code-block:: python

    def articulos_publicados(request):
        articles = Article.objects.filter(status='publicado')
        return render(request, 'articulos/articulos_publicados.html', {'articles': articles})

Se filtran los articulos con estado "publicado" almacenadas en la base de datos con Article.objects.filter(status='publicado')

- manejar_articulos

.. code-block:: python

    def manejar_articulos(request):
        #comprobamos si el usuario es el administrador
        if request.user.is_authenticated: 
            articles = Article.objects.filter(status__in=['pendiente', 'revision', 'aprobado'])
            return render(request, 'articulos/manejar_articulos.html', {'articles': articles})
        return redirect('articulos:index') 

Los usuarios autenticados podran manejar los articulos mediante request.user.is_authenticated

Se obtienen todos los articulos almacenados en la base de datos (con estados pendiente, revision, aprobado)

- ver_articulo

.. code-block:: python

    def ver_articulo(request, article_id):
        article = get_object_or_404(Article, id=article_id)
        
        if article.status in ['pendiente', 'revision']:
            article.status = 'revision'
            article.save()
        
        if request.method == 'POST':
            if 'aceptar' in request.POST:
                article.status = 'aprobado'
                article.save()
            elif 'rechazar' in request.POST:
                article.status = 'rechazado'
                article.save()
            elif 'publicar' in request.POST and request.user.role == 'admin':   
                article.status = 'publicado'
                article.save()
        
        return render(request, 'articulos/ver_articulo.html', {'article': article, 'myRole': request.user.role})

Se obtiene el articulo con el ID correspondiente mediante get_object_or_404(Article, id=article_id). Si no existe, error 404

Cuando el usuario ingrese a la vista de ver_articulo, el articulo cambia de estado a "revision" si esta en "pendiente" o "revision" (article.status = 'revision')

Si se recibe peticion en form de boton Aceptar el estado se establece en "aprobado" (article.status = 'aprobado')

Si se recibe peticion en form de boton Rechazar el estado se establece en "rechazado" (article.status = 'rechazado')

Si se recibe peticion en form de boton Publicar el estado se establece en "publicado" (article.status = 'publicado')


- tablero_kanban

.. code-block:: python

    def tablero_kanban(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()  
        return render(request, 'articulos/kanban.html', {'articles': articles})
    return redirect('login') 

Los usuarios autenticados tendran acceso a la vista de tablero kanban (request.user.is_authenticated)

Se obtiene todos los articulos y se observan sus estados correspondientes (Article.objects.all())


- edit_comentario

.. code-block:: python

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

Se obtiene comentario con el ID correspondiente mediante get_object_or_404(Comentario, id=comentario_id). Si no existe, error 404

Se comprueba que el usuario que quiere editar comentario es el mismo que realizo (comentario.user != request.user:), si no, va a pantalla detail

En la segunda condicion (request.method == 'POST') se compreuba que la solicitud es un envio de formulario

Se crea una instancia de ComentarioForm con los datos y establece el comentario que ya existia como instancia a editar (ComentarioForm(request.POST, instance=comentario))


- delete_comentario

.. code-block:: python

    def delete_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifica que el usuario sea el autor del comentario
    if comentario.user == request.user:
        comentario.delete()
    
    return redirect('articulos:detail', article_id=comentario.article.id)

Se obtiene comentario con el ID correspondiente mediante get_object_or_404(Comentario, id=comentario_id). Si no existe, error 404

Se comprueba que el usuario que quiere eliminar el comentario es el mismo que realizo (comentario.user == request.user)

Se elimina el comentario (comentario.delete())

- create_notification

.. code-block:: python

    def create_notification(user, message):
        Notification.objects.create(user=user, message=message)

Funcion create_notification() que crea una notificación que se visualizar en el sistema

Tiene dos parametros: user y message

El parametro user representa un objeto de tipo usuario. Es util para identificar al receptor de la notificacion

El parametro message representa el mensaje que recibe el usuario a través de una notificacióno


- notifications_view

.. code-block:: python

    def notifications_view(request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        notifications.filter(is_read=False).update(is_read=True)
        paginator = Paginator(notifications, 20)  #muestra hasta 20 notificaciones
        #se obtiene numero de pagina de notificaciones
        page_number = request.GET.get('page')
        notifications_page = paginator.get_page(page_number)
            
        return render(request, 'articulos/notificaciones.html', {'notifications': notifications_page})

Funcion notifications_view() que crea visualizacion de notificaciones en el sistema

La funcion posee el parametro request. Representa la solicitud http que realiza el user

Se filtran las notificaciones con Notification.objects.filter(user=request.user).order_by('-created_at')

Con Paginator se muestran hasta 20 notificaciones por pagina. Si hay mas, pasan a otra pagina - paginator = Paginator(notifications, 20)

A través de page_number = request.GET.get('page') se pueden visualizar las diferentes paginas de notificaciones

Se renderiza notificaciones.html, es decir se utiliza la plantilla para mostrar las notificaciones recibidas con return render(request, 'articulos/notificaciones.html', {'notifications': notifications_page})

- reportes

.. code-block:: python

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

Método reportes() que crea visualizacion de reportes según requerimientos en el sistema

A través de articles = Article.objects.all(), se recuperan los articulos

A través de la variable articles_by_user = Article.objects.filter(status='publicado').values('author__username').annotate(count=Count('id')) se obtiene la cantidad de publicaciones por cada usuario

A través de la variable articles_by_month = Article.objects.filter(status='publicado').annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month') se obtiene la cantidad de publicaciones realizadas por mes

Con return render(...) se renderiza la plantilla y se pasan los datos obtenidos en el metodo en reportes.html

- toggle_like

.. code-block:: python

    def toggle_like(request, article_id):
        article = get_object_or_404(Article, id=article_id)
        Like.toggle_like(article, request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

article = get_object_or_404(Article, id=article_id): se recuperan los articulos (si existen)

Like.toggle_like(article, request.user): permite hacer y deshacer el "Me gusta" del usuario

La pantalla sigue siendo la misma al dar clic a "Me gusta" y esto se logra medainte return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

- cambios_articulo

.. code-block:: python

    def cambios_articulo(request, article_id):
    # Obtener el artículo específico
        article = get_object_or_404(Article, id=article_id)
        
        # Obtener todas las versiones del artículo
        versions = ArticleVersion.objects.filter(article=article).order_by('-change_date')
        params = {
            'article': article,
            'versions': versions
        }
        return render(request, 'articulos/cambios_articulo.html', params)

A través de article = get_object_or_404(Article, id=article_id) se obtiene un articulo con id coincidente a article_id. En el caso de que no existe dicho articulo se genera 404 Not Found

En un articulo se recuperan (filtran) las versiones de un articulo seleccionado (filter) y se muestran en forma cronologica (order_by('-change_date')) en versions = ArticleVersion.objects.filter(article=article).order_by('-change_date')

Se establece params = {'article':article, 'versions':versions} para dar formato a plantilla para mostrar articulo con los cambios y las respectivas versiones que se recuperan en versions

Se establece la comunicacion HTTPS para la plantilla cambios_articulo.html con render y éste recibe el formato params para mostrar la informacion.

Básicamente, sirve para mostrar el historial de versiones de un determinado articulo

- version_detail

.. code-block:: python

    def version_detail(request, article_id, version_id):
        # Obtener el artículo específico
        article = get_object_or_404(Article, id=article_id)
        
        # Obtener la versión específica del artículo
        version = get_object_or_404(ArticleVersion, id=version_id, article=article)
        
        return render(request, 'articulos/version_detail.html', {
            'article': article,
            'version': version
        })

Como parámetros, tenemos el id del artículo y la versión para pasar a la plantilla que muestra la informacióno

A través de article = get_object_or_404(Article, id=article_id) se obtiene un articulo con id coincidente a article_id. En el caso de que no existe dicho articulo se genera 404 Not Found

A través de version = get_object_or_404(ArticleVersion, id=version_id, article=article) se determina la version del articulo que se filtra a través del id de la version que se recibió como dato, además del id del artículo (PRIMERO SE OBTIENE ID DE ARTICULO Y LUEGO ID DE VERSION DE ARTICULO PARA ASOCIAR)

Se muestra plantilla version_detail.html cuando se pasa formato de plantilla mediante 'article' y 'version' luego de generarse una respuesta HTTPS mediante la función render

Básicamente, sirve para mostrar cada campo de una determinada versión de un artículo

..
   .. automodule:: articulos.views
   :members:
   :undoc-members:
   :show-inheritance:

Formularios
-----------

**Descripción de Clases de forms.py**

- ArticleForm

.. code-block:: python

   class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'video','categoria', 'plantilla']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].required = True
        self.fields['plantilla'].queryset = Plantilla.objects.all()
        self.fields['plantilla'].required = True
        self.fields['plantilla'].label_from_instance = lambda obj: obj.titulo  # Mostrar solo el título

Se utiliza ModelForm para heredar formularios basados en modelos de Django

Se define un formulario basado en el modelo Article

La clase Meta, proporciona metainformacion sobre el formulario

Este formulario se asocia al modelo Article

En el formulario se muestran los campos definidos en Article mediante fields = ['title', 'content', 'image', 'video','categoria', 'plantilla']



- PlantillaForm

.. code-block:: python

   class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['titulo', 'descripcion', 'contenido']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

Se utiliza ModelForm para heredar formularios basados en modelos de Django

Se define un formulario basado en el modelo Plantilla

La clase Meta, proporciona metainformacion sobre el formulario

Este formulario se asocia al modelo Plantilla

En el formulario se muestran los campos definidos en Plantilla mediante fields = ['titulo', 'descripcion', 'contenido']

- CategoriaForm

.. code-block:: python

   class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['titulo']

Se utiliza ModelForm para heredar formularios basados en modelos de Django

Se define un formulario basado en el modelo Categoria

La clase Meta, proporciona metainformacion sobre el formulario

Este formulario se asocia al modelo Categoria

En el formulario se muestran los campos definidos en Categoria mediante fields = fields = ['titulo']

- ComentarioForm

.. code-block:: python

    class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'cols': 80}),
        }

Se utiliza ModelForm para heredar formularios basados en modelos de Django

Se define un formulario basado en el modelo Comentario

La clase Meta, proporciona metainformacion sobre el formulario

En el formulario se muestran los campos definidos en Comentario mediante fields = fields = ['content']

..
   .. automodule:: articulos.forms
   :members:
   :undoc-members:
   :show-inheritance:
