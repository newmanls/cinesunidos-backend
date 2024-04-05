from django.db import models


class Movie(models.Model):
    rating_choices = {
        'A': 'A (Todo público)',
        'B': 'B (Mayores de 13 años)',
        'C': 'C (Mayores de 18 años)',
    }

    title = models.CharField('título', max_length=255, unique=True)
    original_name = models.CharField(
        'título original', max_length=255, blank=True, null=True)
    overview = models.TextField('resumen', blank=True, null=True)
    rating = models.CharField(
        'clasificación', max_length=1, choices=rating_choices)
    running_time = models.IntegerField(
        'duración (en minutos)', blank=True, null=True)
    release_date = models.DateField('fecha de estreno', blank=True, null=True)
    poster = models.URLField('poster', blank=True, null=True)
    backdrop = models.URLField('fondo', blank=True, null=True)

    class Meta:
        verbose_name = 'película'
        verbose_name_plural = 'películas'

    def __str__(self):
        return self.name


class Theatre(models.Model):
    name = models.CharField('nombre', max_length=100, unique=True)
    address = models.CharField('dirección', max_length=255)

    class Meta:
        verbose_name = 'cine'
        verbose_name_plural = 'cines'

    def __str__(self):
        return self.name
