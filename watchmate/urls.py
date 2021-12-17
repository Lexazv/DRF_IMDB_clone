from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('User.urls')),
    path('platforms/', include('Platforms.urls')),
    path('films/', include('Films.urls')),
    path('reviews/', include('Reviews.urls')),
]
