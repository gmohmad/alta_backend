from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from .models import UserProfile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)

        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'bio', 'location', 'company')

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop('user', {})

        if username := user_data.pop('username', None):
            user.username = username
        if email := user_data.pop('email', None):
            user.email = email
        user.save()

        instance.__dict__.update(validated_data)
        instance.save()

        return instance
