from django.urls import include, path
from rest_framework import routers

from .views import FilmViewSet, TheaterViewSet

router = routers.DefaultRouter()
router.register(r'films', FilmViewSet)
router.register(r'theaters', TheaterViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
