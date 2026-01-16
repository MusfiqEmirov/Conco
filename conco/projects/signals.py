from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from projects.models import Appeal
from projects.utils import send_mail_func


@receiver(post_save, sender=Appeal)
def send_mail_per_cv_appeal(sender, instance, created, **kwargs):
    if not created:
        return

    subject = 'Website üzərindən CV göndərildi'

    message = f"""
Yeni CV daxil oldu 👇

Vakansiya: {instance.vacancy}
Ad Soyad: {instance.full_name}
Email: {instance.email}
Telefon: {instance.phone_number}

Tarix: {instance.created_at}
    """

    admin_email = settings.EMAIL_HOST_USER  

    send_mail_func(
        user_email=admin_email,
        custom_subject=subject,
        custom_message=message,
        attachment_path=instance.cv.path,  
        attachment_name=instance.cv.name 
    )