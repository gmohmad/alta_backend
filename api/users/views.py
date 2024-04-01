from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import UserProfile
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


@extend_schema(
    tags=['Auth'],
    description='Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.',
)
class MyTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Auth'])
class UserLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(
    tags=['Auth'], description='pass in new user data to create a new user instance'
)
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@extend_schema(tags=['Users'], description='delete current logged in user')
class DeleteUserView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = request.user
        self.perform_destroy(instance)


@extend_schema(tags=['Users'], description='get all user profiles')
class UserProfileListView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@extend_schema(tags=['Users'], description='get the profile of a user')
class UserProfileRetrieveView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@extend_schema(tags=['Users'], description='update the profile of current user')
class UserProfileUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile
