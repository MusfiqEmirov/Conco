import os
from django.db import models
from django.core.validators import FileExtensionValidator

from .vacancy_models import Vacancy

class Appeal(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Vakansiya'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Mail'
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
            models.UniqueConstraint(fields=['vacancy', 'email'], name='unique_cv_per_vacancy')
        ]
        ordering  = ['-created_at']
    
    def __str__(self):
        return self.vacancy.title_az
    
    