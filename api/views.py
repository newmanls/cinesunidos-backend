from rest_framework import permissions, viewsets

from .models import Movie, Theatre
from .serializers import MovieSerializer, TheatreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TheatreViewSet(viewsets.ModelViewSet):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
