from django.urls import path

from .views import ReviewList, ReviewDetail, LikeCreateDelete


urlpatterns = [
    path('list/', ReviewList.as_view(), name='ReviewList'),
    path('<int:review_id>/', ReviewDetail.as_view(), name='ReviewDetail'),
    path(
        '<int:review_id>/like/', LikeCreateDelete.as_view(), name='LikeCreateDelete'
    ),   
]
