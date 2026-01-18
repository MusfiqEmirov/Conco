from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings

from projects.models import Appeal, Project, ProjectCategory, Vacancy, Partner, About, Contact, Media
from projects.utils import send_mail_func
from projects.utils.cache_utils import invalidate_model_cache


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


# Cache invalidation signals for models

@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def invalidate_project_cache(sender, instance, **kwargs):
    """Invalidate cache when Project is saved or deleted."""
    invalidate_model_cache('Project')


@receiver(post_save, sender=ProjectCategory)
@receiver(post_delete, sender=ProjectCategory)
def invalidate_project_category_cache(sender, instance, **kwargs):
    """Invalidate cache when ProjectCategory is saved or deleted."""
    invalidate_model_cache('ProjectCategory')


@receiver(post_save, sender=Vacancy)
@receiver(post_delete, sender=Vacancy)
def invalidate_vacancy_cache(sender, instance, **kwargs):
    """Invalidate cache when Vacancy is saved or deleted."""
    invalidate_model_cache('Vacancy')


@receiver(post_save, sender=Partner)
@receiver(post_delete, sender=Partner)
def invalidate_partner_cache(sender, instance, **kwargs):
    """Invalidate cache when Partner is saved or deleted."""
    invalidate_model_cache('Partner')


@receiver(post_save, sender=About)
@receiver(post_delete, sender=About)
def invalidate_about_cache(sender, instance, **kwargs):
    """Invalidate cache when About is saved or deleted."""
    invalidate_model_cache('About')


@receiver(post_save, sender=Contact)
@receiver(post_delete, sender=Contact)
def invalidate_contact_cache(sender, instance, **kwargs):
    """Invalidate cache when Contact is saved or deleted."""
    invalidate_model_cache('Contact')


@receiver(post_save, sender=Media)
@receiver(post_delete, sender=Media)
def invalidate_media_cache(sender, instance, **kwargs):
    """Invalidate cache when Media is saved or deleted."""
    # Media can affect multiple models, so invalidate all related caches
    invalidate_model_cache('Media')
    
    # Also invalidate related model caches if media belongs to them
    if instance.project:
        invalidate_model_cache('Project')
    if instance.partner:
        invalidate_model_cache('Partner')
    if instance.about:
        invalidate_model_cache('About')
    if instance.vacancy:
        invalidate_model_cache('Vacancy')