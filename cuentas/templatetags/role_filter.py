from django import template

register = template.Library()

@register.filter
def get_role_name(roles_dict, role_key):
    return roles_dict.get(role_key, 'Desconocido')
