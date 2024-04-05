from django.urls import include, path
from rest_framework import routers

from .views import MovieViewSet, TheatreViewSet

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'theatres', TheatreViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
