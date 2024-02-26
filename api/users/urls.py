from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    DeleteUserView,
    LoginView,
    RegisterView,
    UserProfileRetrieveView,
    UserProfileUpdateView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('get-profile/<str:pk>/', UserProfileRetrieveView.as_view(), name='get-profile'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
]
