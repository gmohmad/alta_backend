from django.urls import path

from .views import (
    DeleteUserView,
    MyTokenRefreshView,
    UserLoginView,
    UserProfileListView,
    UserProfileRetrieveView,
    UserProfileUpdateView,
    UserRegisterView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='token-obtain-pair'),
    path('login/refresh/', MyTokenRefreshView.as_view(), name='token-refresh'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('', UserProfileListView.as_view(), name='profile-list'),
    path('<str:pk>/', UserProfileRetrieveView.as_view(), name='retrieve-profile'),

    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
]
