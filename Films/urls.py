from django.urls import path

from .views import FilmList, FilmDetail


urlpatterns = [
    path('list/', FilmList.as_view(), name='FilmList'),
    path('<int:film_id>/', FilmDetail.as_view(), name='FilmDetail'), 
]
