""" from django.test import SimpleTestCase
from categorias.forms import CategoriaForm

class TestForms(SimpleTestCase):
    
    def test_categoria_form_valid_data(self):
        form = CategoriaForm(data={
            'titulo': 'Categoria Test'
        })
        self.assertTrue(form.is_valid())
    
    def test_categoria_form_invalid_data(self):
        form = CategoriaForm(data={
            
        })
        self.assertFalse(form.is_valid()) """