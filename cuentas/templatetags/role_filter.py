from django import template
from cuentas.models import ROLE_CHOICES
register = template.Library()

# Convertir la lista de tuplas a un diccionario
ROLE_CHOICES_DICT = dict(ROLE_CHOICES)

@register.filter
def get_role_name(role_key):
    return ROLE_CHOICES_DICT.get(role_key, 'Desconocido')
