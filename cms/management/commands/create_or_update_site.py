import os
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
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| Sitio Creado:  SITE_NAME={site}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| Sitio Actualizado:  SITE_NAME={site}'))

        # Crear o actualizar la SocialApp para Google
        google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        google_secret = getattr(settings, 'GOOGLE_SECRET', None)

        if not google_client_id or not google_secret:
            self.stdout.write(self.style.ERROR('|GOOGLE SSO| Falta GOOGLE_CLIENT_ID o GOOGLE_SECRET en settings.'))
            return

        social_app, created = SocialApp.objects.update_or_create(
            provider='google',
            name='Google',
            defaults={
                'client_id': google_client_id,
                'secret': google_secret,
            }
        )

        # Asociar el sitio con la SocialApp
        if site not in social_app.sites.all():
            social_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| Sitio {site_name} asociado con SocialApp Google.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| SocialApp Google ya está asociado con "{site_name}".'))

        if created:
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| SocialApp Google creada: CLIENT_ID=>>ESTO ES SECRETO<<'))
        else:
            self.stdout.write(self.style.SUCCESS(f'|GOOGLE SSO| SocialApp Google actualizada: CLIENT_ID=>>ESTO ES SECRETO<<'))