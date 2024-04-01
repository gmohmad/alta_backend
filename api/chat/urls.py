from django.urls import path

from .views import (
    ChatCreateView,
    ChatDeleteView,
    ChatListView,
    MessageListCreateView,
    MessageRUDView,
)

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('create/<str:pk>/', ChatCreateView.as_view(), name='chat-create'),
    path('delete/<str:pk>/', ChatDeleteView.as_view(), name='chat-delete'),

    path('<str:pk>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('<str:ck>/messages/<str:pk>/', MessageRUDView.as_view(), name='message-rud'),
]
