from django.urls import path

from .views import PlatformList, PlatformDetail


urlpatterns = [
    path('list/', PlatformList.as_view(), name='PlatformList'),
    path('<int:platform_id>/', PlatformDetail.as_view(), name='PlatformDetail'),
]
