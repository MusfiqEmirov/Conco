from django.db import models


class Contact(models.Model):
    address_az = models.CharField(
        max_length=255,
        verbose_name='Ünvan (AZ)'
    )
    address_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (EN)'
    )
    address_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (RU)'
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Telefon'
    )
    whatsapp_number = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Whatsapp əlaqə nömrəsi'
    )
    whatsapp_number_2 = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Whatsapp əlaqə nömrəsi 2'
    )
    phone_three = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Telefon'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email'
    )
    instagram = models.URLField(
        null=True,
        blank=True
    )
    facebook = models.URLField(
        null=True,
        blank=True
    )
    youtube = models.URLField(
        null=True,
        blank=True
    )
    linkedn = models.URLField(
        null=True,
        blank=True
    )
    tiktok = models.URLField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqələr"

    def __str__(self):
        return self.address_az or 'Əlaqə'
