from django.shortcuts import get_object_or_404
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
        owner = data.get('owner')
        film = data.get('film')
        if Review.objects.filter(owner=owner, film=film).exists():
            raise ValidationError(detail='user review already exists')
        return data


class ReviewFromURL:

    requires_context = True

    def __call__(self, review_field):
        request = review_field.context.get('request')
        review_id = request.parser_context.get('kwargs').get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review


class LikeSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Like.objects.all(), default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(
        queryset=Like.objects.all(), default=ReviewFromURL()
    )

    class Meta:

        model = Like
        fields = '__all__'

    def validate(self, data):
        owner = data.get('owner')
        review = data.get('review')
        if Like.objects.filter(owner=owner, review=review).exists():
            raise ValidationError(detail='user like already exists')
        return data
