from rest_framework import permissions, viewsets

from .models import Film, Theater
from .serializers import FilmSerializer, TheaterSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
