from django.db import models


class Film(models.Model):
    rating_choices = {
        'A': 'A (Todo público)',
        'B': 'B (Mayores de 13 años)',
        'C': 'C (Mayores de 18 años)',
    }

    name = models.CharField('nombre', max_length=255, unique=True)
    description = models.TextField('descripción', blank=True, default='')
    rating = models.CharField(
        'clasificación', max_length=1, choices=rating_choices)
    running_time = models.IntegerField('duración', blank=True, default='')
    release_date = models.DateField('fecha de estreno', blank=True, null=True)
    poster = models.URLField('poster', blank=True, default='')
    backdrop = models.URLField('fondo', blank=True, default='')

    class Meta:
        verbose_name = 'película'
        verbose_name_plural = 'películas'

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField('nombre', max_length=100, unique=True)
    address = models.CharField('dirección', max_length=255)

    class Meta:
        verbose_name = 'cine'
        verbose_name_plural = 'cines'

    def __str__(self):
        return self.name
