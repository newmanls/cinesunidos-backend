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
        showtimes = Showtime.objects.filter(movie=movie).order_by('theatre__id', 'format')
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
            theatre_id = showtime.theatre.id
            theatre_name = showtime.theatre.name
            theatre_address = showtime.theatre.address
            format = showtime.get_format_display()
            language = showtime.get_language_display()
            format_full = f'{format} ({language})'

            # Check if theatre already exists in theatres list
            theatre_exists = any(theatre['id'] == theatre_id for theatre in theatres)

            if not theatre_exists:
                theatre_data = {
                    'id': theatre_id,
                    'name': theatre_name,
                    'address': theatre_address,
                    'formats': defaultdict(list)
                }
                theatres.append(theatre_data)

            # Find the theatre in the list
            theatre_data = next(theatre for theatre in theatres if theatre['id'] == theatre_id)

            # Append showtime data to the formats list of the theatre
            theatre_data['formats'][format_full].append(ShowtimeSerializer(showtime).data)

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
