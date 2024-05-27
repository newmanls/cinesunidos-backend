from django.db import models


class Movie(models.Model):
    rating_choices = {
        'A': 'A (Todo público)',
        'B': 'B (Mayores de 13 años)',
        'C': 'C (Mayores de 18 años)',
    }

    title = models.CharField(
        'título',
        max_length=255,
        unique=True
    )
    original_title = models.CharField(
        'título original',
        max_length=255
    )
    overview = models.TextField('resumen')
    rating = models.CharField(
        'clasificación',
        max_length=1,
        choices=rating_choices,
        blank=True,
        null=True
    )
    running_time = models.IntegerField(
        'duración (en minutos)',
        blank=True,
        null=True
    )
    release_date = models.DateField(
        'fecha de estreno',
        blank=True,
        null=True
    )
    poster = models.URLField('poster')
    backdrop = models.URLField('fondo')

    class Meta:
        verbose_name = 'película'
        verbose_name_plural = 'películas'

    def __str__(self):
        return self.title


class Theatre(models.Model):
    name = models.CharField(
        'nombre',
        max_length=100,
        unique=True
    )
    address = models.CharField(
        'dirección',
        max_length=255
    )

    class Meta:
        verbose_name = 'cine'
        verbose_name_plural = 'cines'

    def __str__(self):
        return self.name


class Showtime(models.Model):
    format_choices = {
        'digital': 'Digital',
        '3D': '3D',
    }
    language_choices = {
        'es': 'Español',
        'en': 'Inglés',
    }

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name='Película'
    )
    format = models.CharField(
        'formato',
        max_length=30,
        choices=format_choices,
        default=format_choices['digital']
    )
    language = models.CharField(
        'idioma',
        max_length=30,
        choices=language_choices,
        default=language_choices['es']
    )
    theatre = models.ForeignKey(
        Theatre,
        on_delete=models.CASCADE,
        verbose_name='Cine'
    )
    auditorium = models.IntegerField('sala')
    time = models.DateTimeField('hora')

    class Meta:
        verbose_name = 'función'
        verbose_name_plural = 'funciones'

    def __str__(self):
        return f'{self.movie} - {self.get_format_display()} ({self.get_language_display()})'
