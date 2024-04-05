from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Showtime, Theatre
from .serializers import MovieSerializer, ShowtimeSerializer, TheatreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['GET', 'POST'])
    def showtimes(self, request, pk=None):
        movie = self.get_object()
        showtimes = Showtime.objects.filter(movie=movie)
        serializer = ShowtimeSerializer(showtimes, many=True)

        return Response(serializer.data)


class TheatreViewSet(viewsets.ModelViewSet):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
