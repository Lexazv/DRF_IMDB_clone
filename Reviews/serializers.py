from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Review, Like


class ReviewSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Review
        fields = '__all__'

    def validate(self, data):
        if Review.objects.filter(
            owner=data.get('owner'), film=data.get('film')
        ).exists():
            raise ValidationError('user review already exists')


class LikeSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Like.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Like
        fields = '__all__'

    def validate(self, data):
        if Review.objects.filter(
            owner=data.get('owner'), review=data.get('review')
        ).exists():
            raise ValidationError('user like already exists')
