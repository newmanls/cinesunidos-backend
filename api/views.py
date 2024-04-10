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
        theatres = []

        for showtime in showtimes:
            theatre = showtime.theatre
            showtime_data = ShowtimeSerializer(showtime).data
            theatre_data = TheatreSerializer(theatre).data
            theatre_data['showtimes'] = [showtime_data]

            theatre_exists = False
            for existing_theatre in theatres:
                if existing_theatre['id'] == theatre.id:
                    existing_theatre['showtimes'].append(showtime_data)
                    theatre_exists = True
                    break

            if not theatre_exists:
                theatres.append(theatre_data)

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
