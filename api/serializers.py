from rest_framework import serializers

from .models import Movie, Showtime, Theatre


class MovieSerializer(serializers.ModelSerializer):
    running_time = serializers.SerializerMethodField()

    def get_running_time(self, obj):
        hours, minutes = divmod(obj.running_time, 60)

        return f'{hours}h {minutes}m'

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
        fields = ['id', 'time', 'auditorium']
