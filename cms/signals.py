from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def run_create_or_update_site(sender, **kwargs):
    """Run the create_or_update_site command after migrations are applied."""
    if sender.name == 'allauth.socialaccount':
        call_command('create_or_update_site')