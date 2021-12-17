from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from .views import Register, Logout


urlpatterns = [
   path('register/', Register.as_view(), name='register'),
   path('login/', token_obtain_pair, name='login'),
   path('refresh/', token_refresh, name='refresh'),
   path('logout/', Logout.as_view(), name='logout'),
]
