from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Review, Like


class ReviewSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['owner', 'film'],
                message='user review already exists'
            )
        ]


class LikeSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Like.objects.all(), default=serializers.CurrentUserDefault()
    )

    class Meta:

        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields = ['owner', 'review'],
                message='user like already exists'
            )
        ]
