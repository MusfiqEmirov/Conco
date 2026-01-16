import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


from .vacancy_models import Vacancy
from projects.utils import normalize_az_phone

class Appeal(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    
    