# myapp/services/email.py
from django.core.mail import send_mail
import logging
from cuentas.models import CustomUser
from articulos.models import Notification


from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# cms/services/email.py
from cms.services.notifications import create_notification  # Nueva importación


def send_html_email(subject, template_name, context, recipient_list, from_email=None, fail_silently=False):
    """
    Envía un correo electrónico en formato HTML utilizando una plantilla.
    
    :param subject: Asunto del correo.
    :param template_name: Nombre del archivo de plantilla HTML.
    :param context: Contexto para renderizar la plantilla.
    :param recipient_list: Lista de destinatarios.
    :param from_email: Remitente (opcional).
    :param fail_silently: Si debe fallar silenciosamente en caso de error.
    """
    try:
        html_message = render_to_string(template_name, context)
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=from_email,
            to=recipient_list,
        )
        email.content_subtype = 'html'  # Establece el contenido como HTML
        email.send(fail_silently=fail_silently)
        logger.info(f"Correo HTML enviado a: {', '.join(recipient_list)} con asunto: {subject}")
    except Exception as e:
        logger.error(f"Error al enviar correo HTML a: {', '.join(recipient_list)}. Detalles: {e}")


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
    """
    Enviar un correo de confirmación al autor del artículo con soporte HTML.
    """
    author_name = f'{user.first_name} {user.last_name}'.strip()
    subject = f'Notificación de Artículo: {article.title}'
    
    # Determinar el mensaje de notificación
    if action == 'create':
        notification_message = f'Tu artículo "{article.title}" ha sido creado.'
    elif action == 'update':
        notification_message = f'Tu artículo "{article.title}" ha cambiado a estado "{article.status}".'
    else:
        notification_message = f'Actualización en tu artículo "{article.title}".'

    # Contexto para el correo HTML
    context = {
        'user': user,
        'article': article,
        'action': action
    }

    # Enviar correo en formato HTML
    try:
        html_message = render_to_string('articulos/email_notification.html', context)
        email = EmailMessage(
            subject=subject,
            body=html_message,
            to=[user.email]
        )
        email.content_subtype = 'html'  # Establecer el contenido como HTML
        email.send()
        logger.info(f"Correo HTML enviado a {user.email} con asunto: {subject}")
    except Exception as e:
        logger.error(f"Error al enviar correo HTML a {user.email}: {e}")

    # Enviar correo en texto plano como respaldo
    plain_message = f'Hola {author_name},\n\nTu artículo "{article.title}" está ahora en estado "{article.status}".'
    send_cms_email(
        subject=subject,
        message=plain_message,
        recipient_list=[user.email]
    )

    # Crear notificación en la base de datos
    create_notification(user, notification_message)

def send_email_to_role(article, origin, action='create', roles=['editor']):
    from articulos.views import create_notification
    
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
        
        notification_message = f'Un nuevo artículo "{article.title}" ha sido creado por {author_name}.'
        create_notification(u, notification_message)