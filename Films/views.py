from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Film
from .serializers import FilmSerializer


class FilmList(generics.ListCreateAPIView):

    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['platform']


class FilmDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = FilmSerializer

    def get_object(self):
        user = self.request.user
        film = get_object_or_404(Film, pk=self.kwargs.get('film_id'))
        if film.owner == user or user.is_superuser:
            return film
        raise Http404
