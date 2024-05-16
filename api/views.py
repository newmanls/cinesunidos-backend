import json
from collections import defaultdict
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Showtime, Theatre
from .serializers import MovieSerializer, ShowtimeSerializer, TheatreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def showtimes(self, request, pk=None):
        movie = self.get_object()
        movie_serializer = self.get_serializer(movie)
        showtimes = Showtime.objects.filter(movie=movie)
        theatres = defaultdict(dict)

        for showtime in showtimes:
            theatre_id = showtime.theatre.name
            format_id = showtime.get_format_display()
            language = showtime.get_language_display()

            if theatre_id not in theatres:
                theatres[theatre_id] = defaultdict(list)

            theatres[theatre_id][f'{format_id} ({language})'].append(
                    ShowtimeSerializer(showtime).data)

        data = movie_serializer.data
        data['theatres'] = theatres

        return Response(data)


class TheatreViewSet(viewsets.ModelViewSet):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def showtimes(self, request, pk=None):
        theatre = self.get_object()
        theatre_serializer = self.get_serializer(theatre)
        showtimes = Showtime.objects.filter(
                theatre=theatre).order_by('movie__id')
        movies = []

        for showtime in showtimes:
            movie = showtime.movie
            showtime_data = ShowtimeSerializer(showtime).data
            movie_data = MovieSerializer(movie).data
            movie_data['showtimes'] = [showtime_data]

            movie_exists = False
            for existing_movie in movies:
                if existing_movie['id'] == movie.id:
                    existing_movie['showtimes'].append(showtime_data)
                    movie_exists = True
                    break

            if not movie_exists:
                movies.append(movie_data)

        data = theatre_serializer.data
        data['movies'] = movies

        return Response(data)
