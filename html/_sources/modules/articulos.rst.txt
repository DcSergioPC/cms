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
    
    title = models.CharField(max_length=255)
    content = models.TextField()

    ##################
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    ####################
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.title}, {self.content}'

Modelo Article representa la estructura de un articulo en la base de datos

El atributo titulo sera el nombre del articulo. Tendra un tamano maximo de 255 caracteres utilizando CharField

El atributo content almacena el contenido del articulo que se define en la seccion de articulos del proyecto cms

El atributo image permite subir imagenes para los articulos utilizando ImageField (blank=True y null=True indica que es opcional)

El atributo video permite subir videos para los articulos utilizando FileField (blank=True y null=True indica que es opcional)

El atributo categoria es un campo de clave foranea que relaciona el articulo con una categoria Categoria existente. En el caso de que se elimina la categoria, el articulo no se eliminara debido a on_delete=models.SET_NULL, que pondra al campo categoria en NULL

El atributo plantilla es un campo de clave foranea que relaciona el articulo con una plantilla Plantilla existente. En el caso de que se elimina la Plantilla, el articulo no se eliminara debido a on_delete=models.SET_NULL, que pondra al campo Plantilla en NULL


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
         articles = Article.objects.all()
         params = {
            'articles': articles,
         }
         return render(request, 'articulos/index.html', params)

Se obtiene todos los registros de tabla Article que esta almacenada en la base de datos

Se guardan los articulos en diccionario params, donde la clave es 'articles' y el valor es el definido arriba (articles)

Se visualiza la lista de articulos mediante render(request, 'articulos/index.html', params) que renderiza la plantilla pasandole los datos del diccionario

- create

.. code-block:: python

   def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
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
    article = Article.objects.get(id=article_id)
    params = {
        'article': article,
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

..
   .. automodule:: articulos.forms
   :members:
   :undoc-members:
   :show-inheritance:
