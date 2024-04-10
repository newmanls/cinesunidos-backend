from rest_framework import serializers

from .models import Movie, Showtime, Theatre


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['id', 'format', 'language', 'auditorium', 'time']
