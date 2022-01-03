from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Platform
from .serializers import PlatformSerializer


class PlatformList(generics.ListCreateAPIView):

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    pagination_class = LimitOffsetPagination


class PlatformDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PlatformSerializer

    def get_object(self):
        user = self.request.user
        platform = get_object_or_404(
            Platform, pk=self.kwargs.get('platform_id')
        )
        if user == platform.owner or user.is_superuser:
            return platform
        raise Http404
