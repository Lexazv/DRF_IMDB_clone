from rest_framework import serializers

from .models import Platform
from Films.models import Film


class FilmNestedSerializer(serializers.ModelSerializer):

    class Meta:

        model = Film
        fields = ['id', 'title', 'avg_rate']


class PlatformSerializer(serializers.ModelSerializer):

    films = FilmNestedSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(), 
        default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Platform
        fields = '__all__'
