# myapp/services/email.py
from django.core.mail import send_mail
import logging
from cuentas.models import CustomUser

# Obtener el logger personalizado
logger = logging.getLogger('email_logger')

def send_cms_email(subject, message, recipient_list, from_email=None, fail_silently=False):
    """
    Envía un correo electrónico personalizado utilizando send_mail de Django.
    
    :param subject: Asunto del correo.
    :param message: Cuerpo del correo.
    :param recipient_list: Lista de destinatarios.
    :param from_email: Remitente (opcional).
    :param fail_silently: Si debe fallar silenciosamente en caso de error.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )
        # Registrar el envío exitoso
        logger.info(f"Correo enviado exitosamente a: {', '.join(recipient_list)} con asunto: {subject}")
    
    except Exception as e:
        # Registrar el error
        logger.error(f"Error al enviar el correo a: {', '.join(recipient_list)}. Detalles: {e}")

def send_confirmation_email(user, article, action='create'):
    """Enviar un correo de confirmación al autor del artículo."""
    author_name = f'{user.first_name} {user.last_name}'.strip()
    subject = f'Nuevo artículo en estado: {article.status}'
    messageAction = f', tu artículo "{article.title}" ha sido creado exitosamente y está en estado "{article.status}".'

    if(action == 'update'):
        subject = f'Cambio de estado del artículo: {article.title}'
        messageAction = (f'Has realizado un cambio de estado del articulo de "{article.title}" a "{article.status}".\n')
    message = (f'Hola {author_name}'.strip() + ',\n\n' + messageAction)
    send_cms_email(
        subject=subject,
        message=message,
        recipient_list=[user.email]
    )

def send_email_to_role(article, origin, action='create', roles=['editor']):
    """Enviar un correo a todos los usuarios que se encuentren en el array de roles excepto a la persona origin."""
    users = CustomUser.objects.filter(role__in=roles).exclude(id=origin.id)
    # Obtener el nombre del autor del artículo
    author_name = f'{origin.first_name} {origin.last_name}'.strip()

    messageAction = f'Un nuevo artículo "{article.title}" ha sido creado por {author_name} ({origin.email}) y está en estado {article.status}.'
    subject = f'Nuevo artículo en estado: {article.status}'

    if(action == 'update'):
        messageAction = (f'El estado del artículo "{article.title}" ha cambiado a "{article.status}".\n'
                        f'Este cambio fue realizado por: ' + f'{author_name} ({origin.email})'.strip() + '.')
        subject = f'Cambio de estado del artículo: {article.title}'
    
    for u in users:
        message = (f'Hola {u.first_name or ""} {u.last_name or ""}'.strip() + ',\n\n' + messageAction)
        send_cms_email(
            subject=subject,
            message=message,
            recipient_list=[u.email]
        )