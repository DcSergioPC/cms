from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver
# signals.py
from allauth.socialaccount.signals import social_account_added, social_account_updated
from allauth.socialaccount.models import SocialToken, SocialAccount
import jwt

@receiver(post_migrate)
def run_create_or_update_site(sender, **kwargs):
    """Run the create_or_update_site command after migrations are applied."""
    if sender.name == 'allauth.socialaccount':
        call_command('create_or_update_site')

# Helper function to decode Keycloak token
def decode_keycloak_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})  # Decodifica sin verificar la firma
        print(decoded_token)
        return decoded_token
    except jwt.PyJWTError:
        return None

# Signal handler to save the token data after social account is added (first login)
@receiver(social_account_added)
def save_keycloak_data_on_login(sender, request, sociallogin, **kwargs):
    user = sociallogin.user

    # Obtener el token de Keycloak
    try:
        social_account = SocialAccount.objects.get(user=user, provider='keycloak')
        token = SocialToken.objects.get(account=social_account)
        decoded_token = decode_keycloak_token(token.token)
        
        if decoded_token:
            # Guarda la información que necesites en el modelo del usuario o en otro lugar
            user.first_name = decoded_token.get('given_name')
            user.last_name = decoded_token.get('family_name')
            user.save()
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
        pass

# Signal handler to save token data on subsequent logins (account updated)
@receiver(social_account_updated)
def update_keycloak_data_on_login(sender, request, sociallogin, **kwargs):
    user = sociallogin.user

    try:
        social_account = SocialAccount.objects.get(user=user, provider='keycloak')
        token = SocialToken.objects.get(account=social_account)
        decoded_token = decode_keycloak_token(token.token)

        if decoded_token:
            # Actualiza o guarda la información del token como prefieras
            user.first_name = decoded_token.get('given_name')
            user.last_name = decoded_token.get('family_name')
            user.save()
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
        pass