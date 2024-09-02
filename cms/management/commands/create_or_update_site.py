from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

class Command(BaseCommand):
    help = 'Create or update the site with environment variables'

    def handle(self, *args, **kwargs):
        # Obtener el nombre del sitio desde settings
        site_name = getattr(settings, 'SITE_NAME', 'localhost')
        site_id = getattr(settings, 'SITE_ID', 1)

        # Crear o actualizar el sitio
        site, created = Site.objects.update_or_create(
            id=site_id,
            defaults={
                'name': site_name,
                'domain': site_name
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'|KEYCLOAK SSO| Sitio Creado:  SITE_NAME={site}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'|KEYCLOAK SSO| Sitio Actualizado:  SITE_NAME={site}'))