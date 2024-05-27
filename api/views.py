from collections import defaultdict
from datetime import datetime

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
        showtimes = Showtime.objects.filter(
            movie=movie).order_by('theatre__id', 'format', 'time')
        theatres = []

        # Query filters
        query_date = self.request.query_params.get('date')
        query_theatre_id = self.request.query_params.get('theatre_id')

        if query_date is not None:
            showtimes = showtimes.filter(time__date=query_date)
        else:
            showtimes = showtimes.filter(time__date=datetime.now().date())

        if query_theatre_id is not None:
            showtimes = showtimes.filter(theatre__id=query_theatre_id)

        # Output formatting
        for showtime in showtimes:
            theatre_data = TheatreSerializer(showtime.theatre).data
            format = showtime.get_format_display()
            language = showtime.get_language_display()
            format_full = f'{format} ({language})'

            theatre_exists = any(
                theatre['id'] == theatre_data['id'] for theatre in theatres)

            if not theatre_exists:
                theatre_data['formats'] = defaultdict(list)

                theatres.append(theatre_data)

            # Find the theatre in the list
            theatre_data = next(
                theatre for theatre in theatres if theatre['id'] == theatre_data['id'])

            # Append showtime data to the formats list of the theatre
            theatre_data['formats'][format_full].append(
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
            theatre=theatre).order_by('movie__id', 'format', 'time')
        movies = []

        # Query filters query
        query_date = self.request.query_params.get('date')
        query_movie_id = self.request.query_params.get('movie_id')

        if query_date is not None:
            showtimes = showtimes.filter(time__date=query_date)
        else:
            showtimes = showtimes.filter(time__date=datetime.now().date())

        if query_movie_id is not None:
            showtimes = showtimes.filter(movie__id=query_movie_id)

        for showtime in showtimes:
            movie_data = MovieSerializer(showtime.movie).data
            format = showtime.get_format_display()
            language = showtime.get_language_display()
            format_full = f'{format} ({language})'

            movie_exists = any(movie['id'] == movie_data['id']
                               for movie in movies)

            if not movie_exists:
                movie_data['formats'] = defaultdict(list)

                movies.append(movie_data)

            movie_data = next(
                movie for movie in movies if movie['id'] == movie_data['id'])
            movie_data['formats'][format_full].append(
                ShowtimeSerializer(showtime).data)

        data = theatre_serializer.data
        data['movies'] = movies

        return Response(data)
