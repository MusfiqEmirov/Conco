from django.db import models
from django.core.validators import MaxLengthValidator

from projects.utils import SluggedModel


class ProjectCategory(SluggedModel):
    name_az = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (AZ)'
    )
    name_en = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (EN)'
    )
    name_ru = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Kateqoriya adı (RU)'
    )

    class Meta:
        verbose_name = 'Kateqoriya adı'
        verbose_name_plural = 'Kateqoriya adları'
    
    def get_slug_source(self) -> str:
        return self.name_az

    def __str__(self):
        return self.name_az or 'Kateqoriya'


class Project(SluggedModel):
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name='Kateqoriya'
    )
    name_az = models.CharField(
        max_length=250,
        verbose_name='Ad (AZ)'
    )
    name_en = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Ad (EN)'
    )
    name_ru = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Ad (RU)'
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(5000)],
        verbose_name='Layihə haqqında (AZ)'
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Layihə haqqında (EN)'
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Layihə haqqında (RU)'
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Url'
    )
    is_completed = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Layihə tamamlanıb'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name='Layihə aktivliyi'
    )
    speacial_project = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Seçilmiş Lahiyə'
    )
    on_main_page = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Ana səhifədə olsun'
    )
    project_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Layihə yaradılma tarixi'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def get_slug_source(self) -> str:
        return self.name_az

    class Meta:
        verbose_name = 'Layihə'
        verbose_name_plural = 'Layihələr'
        ordering  = ['-created_at']

    def __str__(self):
        return self.name_az
