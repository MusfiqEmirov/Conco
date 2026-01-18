from django.db import models
from django.core.validators import MaxLengthValidator


class Partner(models.Model):
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    name_az = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(120)],
        verbose_name='Əməkdaş adı (AZ)'
    )
    name_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(120)],
        verbose_name='Əməkdaş adı (EN)'
    )
    name_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(120)],
        verbose_name='Əməkdaş adı (RU)'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Əməkdaş aktivliyi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )

    class Meta:
        verbose_name = 'Əməkdaş'
        verbose_name_plural = 'Əməkdaşlar'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name_az or 'Əməkdaş'
