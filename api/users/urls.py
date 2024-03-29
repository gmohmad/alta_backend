from django.urls import path

from .views import (
    DeleteUserView,
    MyTokenRefreshView,
    UserLoginView,
    UserProfileRetrieveView,
    UserProfileUpdateView,
    UserRegisterView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('<str:pk>/', UserProfileRetrieveView.as_view(), name='retrieve-profile'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
]
