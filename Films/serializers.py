from rest_framework import serializers

from .models import Film
from Reviews.models import Review


class ReviewNestedSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Review
        fields = ['id', 'rate', 'owner']


class FilmSerializer(serializers.ModelSerializer):

    reviews = ReviewNestedSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Film
        fields = '__all__'
