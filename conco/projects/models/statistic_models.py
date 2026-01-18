from django.db import models
from django.core.validators import MaxLengthValidator

class Statistic(models.Model):
    value_one = models.PositiveIntegerField(
        verbose_name='Müştəri sayı'
    )
    value_two = models.PositiveIntegerField(
        verbose_name='Layihələr sayi'
    )
    value_three = models.PositiveIntegerField(
        verbose_name='Tərəfdaş sayi'
    )

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'

    def __str__(self):
        return 'Statistika'

   
    
   
