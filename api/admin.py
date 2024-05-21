from django.contrib import admin

from .models import Movie, Showtime, Theatre


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'format', 'language',
                    'theatre', 'auditorium', 'time')
    list_filter = ('movie', 'theatre', 'format', 'language')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_title', 'rating',
                    'running_time', 'release_date')
    list_filter = ('rating', )

class TheatreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Theatre, TheatreAdmin)
admin.site.register(Showtime, ShowtimeAdmin)
