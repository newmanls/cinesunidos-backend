from django.contrib import admin

from .models import Movie, Showtime, Theatre


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'format', 'language',
                    'theatre', 'auditorium', 'time')
    list_filter = ('movie', 'theatre')


admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Showtime, ShowtimeAdmin)
