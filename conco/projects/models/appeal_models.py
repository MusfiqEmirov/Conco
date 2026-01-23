import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.utils import timezone

from .vacancy_models import Vacancy
from projects.utils import normalize_az_phone


class AppealVacancy(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appeal_set',
        verbose_name='Vakansiya'
    )
    full_name = models.CharField(
        null=True,
        blank=True,
        verbose_name='Ad Soyad'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Mail'
    )
    phone_number = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name='Mobil Nömrə'
    )
    info = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name='Əlavə məlumat'
    )

    cv = models.FileField(
        upload_to='cvs/',  
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        verbose_name='CV'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunulub'
    )

    class Meta:
        verbose_name = 'CV'
        verbose_name_plural = 'CV-lər'
        constraints = [
            models.UniqueConstraint(
                fields=['vacancy', 'email'],
                name='unique_email_per_vacancy'
            ),
            models.UniqueConstraint(
                fields=['vacancy', 'phone_number'],
                name='unique_phone_per_vacancy'
            ),
        ]
        ordering  = ['-created_at']

    def clean(self):
        if self.phone_number:
            normalized = normalize_az_phone(self.phone_number)
            if normalized:
                self.phone_number = normalized
            else:
                raise ValidationError({
                    'phone_number': 'Düzgün Azərbaycan mobil nömrəsi deyil.'
                })
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.vacancy.title_az
    

class AppealContact(models.Model):
    full_name = models.CharField(
        null=True,
        blank=True,
        verbose_name='Ad Soyad'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Mail'
    )
    subject = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name='Subyekt'
    )
    info = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(500)],
        max_length=500,
        verbose_name='Əlavə məlumat'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    created_date = models.DateField(
        default=timezone.now
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunulub'
    )

    class Meta:
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.created_date:
            from django.utils import timezone
            self.created_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Mesajlar'