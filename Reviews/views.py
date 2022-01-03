from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Review, Like
from .serializers import ReviewSerializer, LikeSerializer


class ReviewList(generics.ListCreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['film']


class ReviewDetail(generics.RetrieveUpdateAPIView):

    serializer_class = ReviewSerializer

    def get_object(self):
        user = self.request.user
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        if user == review.owner or user.is_superuser:
            return review


class LikeCreateDelete(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = LikeSerializer
    lookup_field = 'review_id'

    def get_queryset(self):
        return Like.objects.filter(
            review=self.kwargs.get('review_id'), owner=self.request.user
        )
