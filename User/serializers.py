from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, \
    BlacklistedToken


class RegistrationSerializer(serializers.ModelSerializer):

    confirmed_password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    class Meta:

        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password_value):
        if password_value != self.initial_data.get('confirmed_password'):
            raise ValidationError(detail='passwords not equal')
        return password_value

    def validate_email(self, email_value):
        if User.objects.filter(email=email_value).exists():
            raise ValidationError(detail='email already exists')
        return email_value

    def create(self, validated_data):
        new_user = User(
            username=validated_data.get('username'), 
            email=validated_data.get('email')
        )
        new_user.set_password(validated_data.get('password'))
        new_user.save()
        return new_user


class CurrentUserRefreshToken:

    requires_context = True

    def __call__(self, token_field):
        refresh_token = get_object_or_404(
            OutstandingToken, user_id=token_field.context.get('request').user
        )
        return refresh_token


class LogoutSerializer(serializers.ModelSerializer):

    token = serializers.CharField(default=CurrentUserRefreshToken())

    class Meta:

        model = BlacklistedToken
        fields = '__all__'
