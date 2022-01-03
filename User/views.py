from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .permissions import NotAuthentficated
from .serializers import RegistrationSerializer, LogoutSerializer


class Register(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [NotAuthentficated]


class Logout(generics.CreateAPIView):
    
    queryset = BlacklistedToken.objects.all()
    serializer_class = LogoutSerializer

