from django.db import models
from django.core.validators import MaxLengthValidator

from projects.utils import SluggedModel


class Vacancy(SluggedModel):
    title_az = models.CharField(
        max_length=250,
        verbose_name='Vakansiya adı (AZ)'
    )
    title_en = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Vakansiya adı (EN)'
    )
    title_ru = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Vakansiya adı (RU)'
    )
    description_az = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(8000)],
        verbose_name='Vakansiya haqqında (AZ)',
    )
    description_en = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(8000)],
        verbose_name='Vakansiya haqqında (EN)',
    )
    description_ru = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(8000)],
        verbose_name='Vakansiya haqqında (RU)',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Vakansiya aktivliyi'
    )

    class Meta:
        verbose_name = 'Vakansiya'
        verbose_name_plural = 'Vakansiyalar'
        ordering  = ['-created_at']
    
    def get_slug_source(self) -> str:
        return self.title_az

    def __str__(self):
        return self.title_az or 'Vakansiya'
